from threading import Thread
import socket # For socket communication
from datetime import datetime # For timestamping messages


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))

        self.clients = []


    def start(self):
        try:
            # Start the server
            self.server_socket.listen(5)
            print(f"Server started on {self.host}:{self.port}")

            while True:
                connection_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr} has been established.")
                thread = Thread(target=self.handle_client, args=(connection_socket,))
                thread.start() 

        except KeyboardInterrupt:
            print("Server shutting down...")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.server_socket.close()

    def pass_message(self, message, sender_socket):
        ''' Send messages to everyone but the sender '''
        for client in self.clients:
            if client != sender_socket:
                client.send(message.encode())


    def handle_client(self, connection_socket):
        ''' Handle communication with one client '''
        while True:
            try:
                message = connection_socket.recv(1024).decode()
                if not message:
                    break
                print(f"Received message: {message}")
                self.pass_message(message)
            except Exception as e:
                print(f"Error: {e}")
                break

        connection_socket.close()
        print("Connection closed.")

    def remove_client(self, connection_socket):
        ''' Remove a client from the list '''
        pass


if __name__ == "__main__":
    host = '127.0.0.1'  # Replace with your host
    port = 5000        # Replace with your port
    server = Server(host, port)
    server.start()



# Provided starting server code 
# def handleClient(sock):
#   # Handle communication with one client

#   # Remember to close the socket when done
#   sock.close()

# server_socket.listen(___)
# while True:
#   connection_socket, _ = server_socket.accept()
#   t = Thread(target = handleClient, args=(connection_socket,))
#   t.start()
# server_socket.close()