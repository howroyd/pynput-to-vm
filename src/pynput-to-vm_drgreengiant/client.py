import dataclasses
import socket

from . import messagetypes


@dataclasses.dataclass(slots=True)
class Client:
    address: str
    port: int
    sock: socket.socket = None
    server: tuple[socket.socket, str] = None

    def on_bytes(self, data):
        msg = messagetypes.Message.fromJSON(data)
        print(msg)

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.address, self.port))
        self.sock.listen()
        self.server = self.sock.accept()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()
        return False
