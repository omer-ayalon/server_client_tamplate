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

    async def run_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self._host, self._port))

        client_socket.send(f'{self._username}'.encode('utf-8'))

        self._loop.create_task(self.recv_handler(client_socket))
        await self._loop.create_task(self.send_handler(client_socket))

    async def send_handler(self, client_socket):
        while True:
            massage = await ainput('>>')
            # massage = await input('>>')
            client_socket.send(massage.encode('utf-8'))

    async def recv_handler(self, client_socket):
        while True:
            data = await self._loop.sock_recv(client_socket, 1024)
            data = data.decode('utf-8')
            if data == '':
                raise Exception('Server Is Down')
            print(data)



# def main():
loop = asyncio.new_event_loop()
# loop = asyncio.get_event_loop()
client = Client('192.168.1.42', 5048, 'PC', loop)  # '127.0.0.1'
loop.run_until_complete(client.run_client())
# asyncio.run(client.run_client())

# if __name__ == '__main__':
#     main()
