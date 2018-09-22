import zmq
import sys
import random
import hashlib
import ast

partSize = 1024 * 1024 * 1

def uploadFile2(filename, socket):
    with open(filename, "rb") as f:
        finished = False
        part = 0
        while not finished:
            print("Uploading part {}".format(part))
            f.seek(part*partSize)
            bt = f.read(partSize)
            socket.send_multipart([filename, bt])
            response = socket.recv()
            print("Received reply  [%s ]" % (response))
            part = part + 1
            if len(bt) < partSize:
                finished = True

def computeHashFile(filename):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def computeHash(bytes):
    sha1 = hashlib.sha1()
    sha1.update(bytes)
    return sha1.hexdigest()

def uploadFile(context, filename, servers, username, proxy):
    sockets = []
    for ad in servers:
        s = context.socket(zmq.REQ)
        s.connect("tcp://"+ ad.decode('ascii'))
        sockets.append(s)

    with open(filename, "rb") as f:
        completeSha1= bytes(computeHashFile(filename), 'ascii')
        finished = False
        part = 0
        index = open("1.txt","w+")
        index.write(filename.decode('ascii') + "\n")
        # index.write(completeSha1.decode('ascii') + "\n")
        auxDict = {}

        while not finished:
            print("Uploading part {}".format(part))
            f.seek(part*partSize)
            bt = f.read(partSize)
            sha1bt = bytes(computeHash(bt), 'ascii')
            #auxDict llave = sha1 de la parte; valor = servidor de la parte
            auxDict[sha1bt] = servers[part % len(sockets)]
            index.write(sha1bt.decode('ascii') + "\n")
            s = sockets[part % len(sockets)]
            s.send_multipart([b"upload", filename, bt, sha1bt, completeSha1])
            response = s.recv()
            # print(response)
            print("Received reply for part {} ".format(part))
            part = part + 1
            if len(bt) < partSize:
                finished = True
        
        index.close()
        ShaIndex = bytes(computeHashFile("1.txt"), 'ascii')
        print(ShaIndex)
        #Envio del archivo index a uno de los servidores
        serverIndex = random.randint(0, len(sockets)-1)
        with open("1.txt", "rb") as f:
            s = sockets[serverIndex]
            s.send_multipart([b"upload", b".txt", f.read(), ShaIndex, completeSha1])
        
        #Envio de auxDict, el sha1 de index y quien lo tiene, 
        proxy.send_multipart([b"finished", bytes(str(auxDict),'ascii'), ShaIndex, servers[serverIndex], bytes(username, 'ascii'), filename])

def downloadFile(context, shaIndex, dictIndex,locatIndex, servers):
    sockets = {}
    
    for ad in servers:
        s = context.socket(zmq.REQ)
        s.connect("tcp://"+ ad.decode('ascii'))
        sockets[ad] = s
    
    sockets[locatIndex].send_multipart([b"download", shaIndex])
    msg = sockets[locatIndex].recv_multipart()
    fileIndex = msg[0].decode('ascii')
    fileIndex = fileIndex.split("\n")
    # print(fileIndex)
    # print(dictIndex)
    for i, line in enumerate(fileIndex):
        if i < 1:
            finFile = open(line, "ab")
            name = line
            continue
        if i < len(fileIndex)-1:
            key = line.encode('ascii')
            locatPart = dictIndex[key]
            print(locatPart)
            sock = sockets[locatPart]
            print(sock)
            sock.send_multipart([b"download", key])
            partFile = sock.recv_multipart()
            finFile.write(partFile[0])
    finFile.close()
    return name
    

def main():
    if len(sys.argv) != 4:
        print("Must be called with a filename")
        print("Sample call: python ftclient <username> <operation> <filename>")
        exit()


    username = sys.argv[1]
    operation = sys.argv[2]
    filename = sys.argv[3].encode('ascii')

    context = zmq.Context()
    proxy = context.socket(zmq.REQ)
    proxy.connect("tcp://localhost:6666")

    print("Operation: {}".format(operation))
    if operation == "upload":
        proxy.send_multipart([b"availableServers"])
        servers = proxy.recv_multipart()
        print("There are {} available servers".format(len(servers)))
        uploadFile(context, filename, servers, username, proxy)
        print("File {} was uploaded.".format(filename.decode('ascii')))
    elif operation == "download":
        proxy.send_multipart([b"serverIndex", filename])
        infDownload = proxy.recv_multipart()
        shaIndex = infDownload[0]
        dictIndex = eval(infDownload[1])
        locatIndex = infDownload[2]
        servers = eval(infDownload[3])
        # print(shaIndex)
        # print("###########")
        # print(dictIndex)
        # print("###########")
        # print(locatIndex)
        # print("###########")
        # print(servers)
        nameFile = downloadFile(context, shaIndex, dictIndex,locatIndex, servers)
        print("The {} has been downloaded". format(nameFile))

    elif operation == "tolist":
        proxy.send_multipart([b"tolist", bytes(username, 'ascii')])
        msg = proxy.recv_multipart()
        listFiles = eval(msg[0].decode('ascii'))
        for i in listFiles:
            print(i)

    elif operation == "share":
        print("Not implemented yet")
        
    else:
        print("Operation not found!!!")

if __name__ == '__main__':
    main()
