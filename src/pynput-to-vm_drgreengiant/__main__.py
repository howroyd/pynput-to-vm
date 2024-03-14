import contextlib
import time

import pynput
from typing import Callable
from . import server, client


def make_listeners(server) -> set[Callable]:
    return {
        lambda: pynput.keyboard.Listener(on_press=server.on_press, on_release=server.on_release),
        lambda: pynput.mouse.Listener(on_move=server.on_move),
        lambda: pynput.mouse.Listener(on_click=server.on_button),
    }


if __name__ == "__main__":
    mode = input("Server or Client [s or c]? ").lower()

    if mode == "s":
        myserver = server.Server("192.168.179.128", 60666)

        listeners = [
            lambda: pynput.keyboard.Listener(on_press=myserver.on_press, on_release=myserver.on_release),
            lambda: pynput.mouse.Listener(on_move=myserver.on_move),
            lambda: pynput.mouse.Listener(on_click=myserver.on_button),
        ]

        with contextlib.ExitStack() as stack:
            stack.enter_context(myserver)
            [stack.enter_context(listener()) for listener in listeners]

            while True:
                time.sleep(1)

    elif mode == "c":
        with client.Client("localhost", 12345) as myclient:
            myclient.on_bytes(myclient.sock.recv(1024))
