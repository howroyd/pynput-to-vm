import dataclasses
import socket

from . import messagetypes


@dataclasses.dataclass(slots=True)
class Server:
    address: str
    port: int
    sock: socket.socket = None

    def on_press(self, key):
        msg = messagetypes.make_message(messagetypes.make_keyboard_event(key, True))
        self._send(msg)

    def on_release(self, key):
        msg = messagetypes.make_message(messagetypes.make_keyboard_event(key, False))
        self._send(msg)

    def on_move(self, x, y):
        msg = messagetypes.make_message(messagetypes.make_mouse_move_event(x, y))
        self._send(msg)

    def on_button(self, button, pressed):
        msg = messagetypes.make_message(messagetypes.make_mouse_button_event(button, pressed))
        self._send(msg)

    def _send(self, msg):
        # self.sock.sendall(msg.toJSON())
        print(msg.toJSON())

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.address, self.port))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()
        return False
