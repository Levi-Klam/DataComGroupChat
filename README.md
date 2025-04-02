# DataComGroupChat

## Functionality
1. The server starts and listens for incoming client connections.
2. A client starts the application, enters a username and connects to the server. The username is then sent to the server to announce to the group chat they connected.
3. Messages from the client are sent to the server, which broadcasts them to the other connected clients.
4. The GUI is automatically updated with incoming messages.
5. When a client disconnects, the server removes them form the active list and notifies other clients.


## Dependencies
- Python 3.x
- Tkinter


## server.py
### Class: Server
The **Server** class is responsible for managing multiple client connections, broadcasting messages from those clients, and handling disconnections.

### Attributes:
self.host (str): The server's IP address.
self.port (int): The port number to listen on
self.server_socket (socket): The main server socket that listens for incoming connections
self.clients (dict): Stores connected clients, formatted as {username, socket}.
self.lock (threading lock): Ensures thread-safe access to the **clients** dictionary for concurrent use.

### Methods:
__init(self, host, port):__ Initialize the server, set up the socket, adn bind to the specified host and port.
__start(self):__ Start the server, listen for client connection and create a new thread for each new client.
__handle_client(self, connection_socket):__ Handle communication with each individual client.
__pass_message(self, message, sender_socket):__ Send new messages to all clients besides the original sender.
__remove_client(self, username):__ Removes a client from the active clients list and notifies the groupchat of the disconnection.


## groupchat.py
### Class: App
The **App** class provides a graphical interface for the user to send and receive messages in the chat. It handles all communication with the server while providing a clean front-end.

### Attributes:
self.master (tl.Tk): The main Tkinter window.
self.socket (socket): The client's connection to the server.
self.username (str): The username of the client.
self.data_queue (queue.Queue): Stores incoming messages from the server.
self.running (bool): Controls the application's execution state.
self.socket_thread (threading.Thread): Handles receiving messages in the background.

### Methods:
__init(self, master):__ Initializes the GUI, calls the get_username() function and starts the socket thread once a username is input.
__get_username(self): Opens a prompt window to get the user's username.
__read_socket(self):__ Manages the socket connection, sends the username to the server and listens for messages from the server.
__setup_gui(self):__ Creates the chat display, input field, and send button.
__update_gui(self):__ Check for new messages and update the chat window periodically.
__update_chat(self, message):__ Update the chat disply with new messages.
__send_message(self):__ Send client messages to the server to be distributed.
__close(self):__ Clean up the resources used and close the application.




## Running the Application
1. Start the server:
   '''
   python server.py
   '''
2. Start the client:
   '''
   python groupchat.py
   '''
