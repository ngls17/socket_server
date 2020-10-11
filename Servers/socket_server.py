from datetime import datetime
import json
import socket
import string
import time

from models import ReturnedString, Statistics


class SocketServer:

    def __init__(self, port=5555):
        self.port = port
        self.cid = 0
        self.serv_sock = self.create_serv_sock()
        self.client_sock = None
        self.start_time = None
        self.end_time = None

    def run_server(self):
        """Main method for connect and process client"""
        while True:
            self.client_sock = self.accept_client_conn()
            self.start_time = datetime.now()
            self.serve_client()
            self.cid += 1

    def create_serv_sock(self):
        """Create server socket"""
        serv_sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  proto=0)
        serv_sock.bind(('', self.port))
        serv_sock.listen()
        return serv_sock

    def accept_client_conn(self):
        """Establish connection with client"""
        client_sock, client_addr = self.serv_sock.accept()
        print(f'Client #{self.cid} connected '
              f'{client_addr[0]}:{client_addr[1]}')
        return client_sock

    def serve_client(self):
        """Process client"""
        request = self.process_request()
        # Show message when client is unexpectedly disconnected
        if request is None:
            print(f'Client #{self.cid} unexpectedly disconnected')
        else:
            self.write_response(b'It is the end, thanks')
            self.end_time = datetime.now()

            # Create data for write in file
            result = {
                "work_time": str(self.end_time - self.start_time),
                "string_count": ReturnedString.find_by_time(self.start_time, self.end_time),
                "statistics": {row.char: {"count": row.count, "count_at_first_place": row.count_at_first_place} for row
                               in Statistics.get_table()}
            }
            with open('result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

    def process_request(self):
        """Send to client request and save returned string in db"""
        try:
            while True:
                # Send request to client and decode received string
                self.send_to_client()
                chunk = self.client_sock.recv(16).decode()
                # Return if Client unexpectedly disconnected
                if not chunk:
                    return None

                # Save str to db and write statistics
                ReturnedString.add(text=chunk)
                for index, char in enumerate(chunk):
                    stat_row = Statistics.find(char=char)
                    if stat_row:
                        Statistics.update(char=char, count_at_first_place=1 if index == 0 else 0)
                    else:
                        Statistics.add(char=char, count=1, count_at_first_place=1 if index == 0 else 0)
                # Get statistics from db
                count_at_first_place_all = {row.char: row.count_at_first_place for row in Statistics.get_table()}
                # Check if all letters was received at first position
                if set(count_at_first_place_all.keys()) == set(string.ascii_lowercase) and all(
                        value > 0 for value in count_at_first_place_all.values()):
                    return True

        except ConnectionResetError:
            # Connection was unexpectedly closed.
            return None
        except:
            raise ConnectionError

    def write_response(self, response):
        """Send message for client if it is end of the session"""
        self.client_sock.sendall(response)
        self.client_sock.close()
        print(f'Client #{self.cid} has been served')

    def send_to_client(self):
        """Send request for client every 2 seconds"""
        self.client_sock.send(b'send me string(16)')
        time.sleep(2)
