import time
import socket


class ClientError(Exception):
    """Исключение клиента"""


class ClientSocketError(ClientError):
    """Сетевое исключение клиента"""


class ClientProtocolError(ClientError):
    """Исключение ошибки протокола клиента"""


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientSocketError("create connection error", err)


    def _read(self):
        data = ""
        while not data.endswith("\n\n"):
            try:
                data +=  self.connection.recv(1024).decode("utf8")
            except socket.error as err:
                raise ClientSocketError("recv data error", err)

        status, payload = data.split("\n", 1)
        payload = payload.strip()

        if status == "error":
            raise ClientProtocolError(payload)

        return payload


    def put(self, key, value, timestamp=str(int(time.time()))):
        try:
            self.connection.sendall("put {key} {value} {timestamp}\n"
                         .format(key=key, value=value, timestamp=str(timestamp)).encode("utf8"))
        except socket.error as err:
            raise ClientSocketError("send data error", err)

        self._read()


    def get(self, key):
        try:
            self.connection.sendall("get {key}\n".format(key=key).encode("utf8"))
        except socket.error as err:
            raise ClientSocketError("data send error", err)

        data = self._read().split("\n")

        answer = {}

        if data[0] == "":
            return answer

        for line in data:
            key, value, timestamp = line.split()
            if key != '':
                if key not in answer:
                    answer[key] = []
                answer[key].append((int(timestamp), float(value)))

        for key in answer:
            answer[key].sort(key=lambda item: item[0])

        return answer

    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientSocketError("close connection error", err)


client = Client("127.0.0.1", 8888, timeout=5)
client.put("test", 0.7, timestamp=1)
client.put("test", 2.0, timestamp=2)
client.put("test", 0.5, timestamp=3)
client.put("load", 3, timestamp=4)
client.put("load", 4, timestamp=5)
print(client.get("*"))

client.close()