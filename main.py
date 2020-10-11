import json

from Servers.socket_server import SocketServer
from Servers.threading_server import ThreadServer

if __name__ == '__main__':
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    if config.get('use_threads'):
        server = ThreadServer(port=5555)
        server.run_server_threaded()
    else:
        server = SocketServer(port=5555)
        server.run_server()
