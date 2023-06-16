import socket
import asyncio


class Server:
    HOST = '192.168.1.42'  # '127.0.0.1'
    PORT = 5048

    def __init__(self, loop):
        self._loop = loop
        self.cliend_list = []

    async def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((Server.HOST, Server.PORT))
        server_socket.listen()
        # server_socket.setblocking(False)

        while True:
            client_socket, addr = await self._loop.sock_accept(server_socket)
            self.cliend_list.append(client_socket)
            print(len(self.cliend_list))
            print(f'Accepted: {addr}')
            user_name = await self._loop.sock_recv(client_socket, 1024)
            user_name = user_name.decode("utf-8")
            print(f'{user_name} Connected')

            self._loop.create_task(self.client_handler(client_socket, user_name))

    def remove_client(self, user_name, client_socket):
        print(f'{user_name} Disconnected')
        idx_to_del = next(i for i, x in enumerate(self.cliend_list) if x == client_socket)
        del self.cliend_list[idx_to_del]

    async def client_handler(self, client_socket, user_name):
        try:
            while True:
                data = await self._loop.sock_recv(client_socket, 1024)

                if data.decode('utf-8') == '':
                    raise ConnectionResetError()

                print(f'Server Received Massage From: {user_name}')
                for receiving_client in self.cliend_list:
                    # if client_socket != receiving_client:
                    receiving_client.send(data)
        except ConnectionResetError:
            self.remove_client(user_name, client_socket)


def main():
    loop = asyncio.new_event_loop()
    server = Server(loop)
    try:
        loop.run_until_complete(server.run_server())
    except KeyboardInterrupt:
        raise Exception('You Closed The Server')


if __name__ == '__main__':
    main()
