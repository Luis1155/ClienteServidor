import zmq
import sys
import hashlib

partSize = 1024 * 1024 * 10

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

def createIndex(filename, servers):
    with open(filename, "rb") as f:
        completeSha1 = computeHashFile(filename) + ".txt"
        with open(completeSha1, "w") as i:    
            finished = False
            part = 0
            while not finished:
                print("Writing part {}".format(part))
                f.seek(part*partSize)
                bt = f.read(partSize)
                sha1bt = computeHash(bt)
                i.write(sha1bt + " " + servers[part % len(servers)].decode("ascii"))
                i.write("\n")
                part = part + 1
                if len(bt) < partSize:
                    finished = True

def uploadFile(context, filename, servers):
    sockets = []
    for ad in servers:
        s = context.socket(zmq.REQ)
        s.connect("tcp://"+ ad.decode("ascii"))
        sockets.append(s)

    with open(filename, "rb") as f:
        completeSha1= bytes(computeHashFile(filename), "ascii")
        finished = False
        part = 0
        while not finished:
            print("Uploading part {}".format(part))
            f.seek(part*partSize)
            bt = f.read(partSize)
            sha1bt = bytes(computeHash(bt), "ascii")
            s = sockets[part % len(sockets)]
            s.send_multipart([b"upload", filename, bt, sha1bt, completeSha1])
            response = s.recv()
            print("Received reply for part {}".format(response))
            part = part + 1
            if len(bt) < partSize:
                finished = True

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
        createIndex(filename, servers)
        print("There are {} available servers".format)
        uploadFile(context, filename, servers)
    elif operation == "download":
        print("Not implemented yet")
    elif operation == "share":
        print("Not implemented yet")
    else:
        print("Operation not found!!!")

if __name__ == '__main__':
    main()
