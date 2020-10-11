import random
import socket
import string


class Client:
    @staticmethod
    def run_client():
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('127.0.0.1', 5555))

        while True:
            data = client_sock.recv(1024).decode()
            if data == 'send me string(16)':
                result_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(16))
                client_sock.sendall(result_str.encode())
            else:
                break

        client_sock.close()
        print('Received', repr(data))


if __name__ == '__main__':
    client = Client()
    client.run_client()
