import threading

from Servers.socket_server import SocketServer
from Clients.simple_client import Client


class ThreadServer(SocketServer):

    def run_server_threaded(self):
        server_thread = threading.Thread(target=self.run_server)
        client_thread = threading.Thread(target=self.run_client)
        server_thread.start()
        client_thread.start()

    @staticmethod
    def run_client(): Client.run_client()
