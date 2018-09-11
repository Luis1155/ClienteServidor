import zmq

def main():
    # Address for each server to receive files
    servAddresses = []
    dataBase = {}
    dataBase2 = {}

    context = zmq.Context()
    servers = context.socket(zmq.REP)
    servers.bind("tcp://*:5555")

    clients = context.socket(zmq.REP)
    clients.bind("tcp://*:6666")

    poller = zmq.Poller()
    poller.register(servers, zmq.POLLIN)
    poller.register(clients, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())
        if clients in socks:
            print("Message from client")
            operation, *msg = clients.recv_multipart()
            if operation == b"availableServers":
                clients.send_multipart(servAddresses)
            elif operation == b"finished":
                dictSeg = eval(msg[0])
                ShaIn = msg[1]
                AddressIndexSha = msg[2]
                Owner = msg[3]
                filename = msg[4].decode("ascii")
                for key,value in dictSeg.items():
                    dataBase[key] = value
                dataBase[ShaIn] = AddressIndexSha
                dataBase2[filename] = [ShaIn, Owner]
                print(dataBase)
                print()
                print(dataBase2)

        if servers in socks:
            print("Message from server")
            operation, *rest = servers.recv_multipart()
            if operation == b"newServer":
                servAddresses.append(rest[0])
                print(servAddresses)
                servers.send(b"Ok")


if __name__ == '__main__':
    main()
