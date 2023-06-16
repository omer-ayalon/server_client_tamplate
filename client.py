import datetime
import socket
import asyncio
import sys
from aioconsole import ainput


class Client:
    def __init__(self, HOST, PORT, user_name, loop):
        self._host = HOST
        self._port = PORT
        self._username = user_name
        self._loop = loop
        self.exit = False

    def print_massage(self, massage):
        date_and_time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        print(f'{date_and_time} {massage}')

    async def run_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self._host, self._port))

        client_socket.send(f'{self._username}'.encode('utf-8'))

        self._loop.create_task(self.recv_handler(client_socket))
        await self._loop.create_task(self.send_handler(client_socket))

    async def send_handler(self, client_socket):
        while True:
            massage = await ainput('')
            # massage = await input('>>')
            massage = f'{self._username} : {massage}'
            client_socket.send(massage.encode('utf-8'))

    async def recv_handler(self, client_socket):
        while True:
            massage = await self._loop.sock_recv(client_socket, 1024)
            massage = massage.decode('utf-8')
            if massage == '':
                raise Exception('Server Is Down')
            self.print_massage(massage)


def main():
    loop = asyncio.new_event_loop()
    client = Client('192.168.1.42', 5048, 'Omer', loop)  # '127.0.0.1'
    loop.run_until_complete(client.run_client())


if __name__ == '__main__':
    main()
