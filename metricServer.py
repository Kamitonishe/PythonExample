import asyncio

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

class DataStorage:

    def __init__(self):
        self._data = {}

    def put(self, key, value, timestamp):
        if key not in self._data:
            self._data[key] = []
        self._data[key].append((int(timestamp), float(value)))
        #print("New data:")
        #print(key)
        #print(self.data[key])


    #palm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n
    def get(self, key):
        answer = ""

        if key == '*':
            #print("***")
            for data_key in self._data:
                data = self._data[data_key]
                for timestamp, value in data:
                    answer += "{key} {value} {timestamp}\n"\
                        .format(key=data_key, value=float(value), timestamp=int(timestamp))

        elif key in self._data:
            data = self._data[key]

            for timestamp, value in data:
                answer += "{key} {value} {timestamp}\n"\
                    .format(key=key, value=float(value), timestamp=int(timestamp))

        return answer




class ClientServerProtocol(asyncio.Protocol):
    storage = DataStorage()


    def connection_made(self, transport):
        self.transport = transport

    #ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n
    #ok\n\n

    #put <key> <value> <timestamp>\n
    #get <key>\n



    def process_data(self, data):
        # indexes:
        ix_command = 0
        ix_key = 1
        ix_value = 2
        ix_timestamp = 3

        answer = ""
        data = data.strip().split(" ")
        if data[ix_command] == "get":
            #print("process_data get")
            answer = "ok\n{storage_data}\n".format(storage_data=ClientServerProtocol.storage.get(data[ix_key]))

        elif data[ix_command] == "put":
            try:
                ClientServerProtocol.storage.put(data[ix_key], data[ix_value], data[ix_timestamp])
                answer = "ok\n\n"
            except:
                answer = "error\nwrong command\n\n"

        else:
            answer = "error\nwrong command\n\n"

        #print("Answer: " + answer)

        return answer


    def data_received(self, data):
        #print("Incoming data: " + data.decode())
        resp = self.process_data(data.decode())
        #print("Resp: " + resp)
        self.transport.write(resp.encode())


#run_server("127.0.0.1", 8888)

#data = DataStorage()
#data.put("test", 0.5, 1)
#data.put("test", 2.0, 2)
#data.put("test", 0.5, 3)
#print(data.get("test"))

