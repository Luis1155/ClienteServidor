import zmq

def main():
    # Address for each server to receive files
    servAddresses = []
    dataParts = {}
    dataIndex = {}
    dataOwner = {}

    context = zmq.Context()
    
    servers = context.socket(zmq.REP)
    servers.bind("tcp://*:5555")

    clients = context.socket(zmq.REP)
    clients.bind("tcp://*:6666")

    poller = zmq.Poller()
    poller.register(servers, zmq.POLLIN)
    poller.register(clients, zmq.POLLIN)

    while True:
        socks = dict(poller.poll(10))
        if clients in socks:
            print("Message from client")
            operation, *msg = clients.recv_multipart()
            if operation == b"availableServers":
                clients.send_multipart(servAddresses)
            elif operation == b"finished":
                dictSeg = eval(msg[0])
                ShaIn = msg[1]
                AddressIndexSha = msg[2]            #Servidorq'contiene archivo
                Owner = msg[3]                      #Propietario
                filename = msg[4].decode('ascii')   #nombreArchivo
                dataParts[ShaIn] = dictSeg
                dataIndex[ShaIn] = AddressIndexSha
                if Owner in dataOwner:
                    dataOwner[Owner].append(filename)
                else:
                    dataOwner[Owner] = [filename]
                clients.send(b"Ok")
                # print(dataParts)
                # print("########")
                # print(dataIndex)
                print("########")
                print(dataOwner)
            elif operation == b"serverIndex":
                shaIndex = msg[0]
                dictIndex = dataParts[shaIndex]
                locatIndex = dataIndex[shaIndex]
                clients.send_multipart([shaIndex, bytes(str(dictIndex),'ascii'), locatIndex, bytes(str(servAddresses), 'ascii')])
            elif operation == b"tolist":
                username = msg[0]
                listFiles = dataOwner[username]
                clients.send_multipart([bytes(str(listFiles), 'ascii')])


        if servers in socks:
            print("Message from server")
            operation, *rest = servers.recv_multipart()
            if operation == b"newServer":
                servAddresses.append(rest[0])
                print(servAddresses)
                servers.send(b"Ok")


if __name__ == '__main__':
    main()
