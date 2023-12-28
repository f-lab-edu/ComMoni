import socket
import orjson
import psutil


class CreateCommanageData:
    def __init__(self, user_id: str, host_name: str):
        self.user_id = user_id
        self.host_name = host_name
        self.host_ip = str(socket.gethostbyname(socket.gethostname()))
        self.memory = str(psutil.virtual_memory().total / (1024 ** 3))
        self.disk = str(psutil.disk_usage("/").total / (1024 ** 3))

    def make(self) -> bytes:
        return orjson.dumps({
            "user_id": self.user_id,
            "host_name": self.host_name,
            "host_ip": self.host_ip,
            "memory": self.memory,
            "disk": self.disk
        })
