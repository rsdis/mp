import asyncio
import datetime
import random
import websockets
import threading
import time
import queue


class web_socket_server:
    def __init__(self, port):
        self.__ws_port = port
        self.__outbound = {}

    def __host_worker(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websockets.serve(
            self.__send_handler, '127.0.0.1', self.__ws_port))
        loop.run_forever()

    async def __send_handler(self, ws, path):
        while True:
            try:
                key = hash(ws)
                if self.__outbound.get(key) is None:
                    self.__outbound[key] = queue.Queue()
                if ws.open:
                    while not self.__outbound[key].empty():
                        msg = self.__outbound[key].get()
                        await ws.send(msg)
                    await asyncio.sleep(1)
                else:
                    self.__outbound.pop(key)
                    return
            except Exception as err:
                print(err)

    def start(self):
        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=self.__host_worker, args={loop})
        thread.start()

    def send(self, msg):
        for key in self.__outbound.keys():
            self.__outbound[key].put(msg)


instance = web_socket_server(9999)
