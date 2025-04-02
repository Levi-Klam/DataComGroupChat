import tkinter as tk
import threading
import socket
import queue
from tkinter import scrolledtext # Found this for scrolling text area

class App:
    def __init__(self, master):
        self.master = master
        master.title("Socket Reader")

        self.socket = None
        self.username = None
        self.get_username()

        self.label_text = tk.StringVar() 
        self.label = tk.Label(master, textvariable = self.label_text)
        self.label.pack()

        self.data_queue = queue.Queue() 
        self.running = True

        self.socket_thread = threading.Thread(target=self.read_socket)
        self.socket_thread.daemon = True  # Allow program to exit even if thread is running
        self.socket_thread.start()

        self.setup_gui()  
        self.update_gui()

    # Open a new window to get a username from client
    def get_username(self):
        name_window = tk.Toplevel(self.master) 
        name_window.title("Username")
        name_window.geometry("300x100")
        name_window.transient(self.master)  # Makes it the secondary window
        name_window.grab_set()  # Can't interact with the main window until this one is closed

        tk.Label(name_window, text="Enter your username:").pack(pady=10) 

        # Input field for username
        name = tk.StringVar() 
        name_entry = tk.Entry(name_window, textvariable=name)
        name_entry.pack(pady=10)
        name_entry.focus_set() # Puts this window on top of the main window

        # The submit button sets the client's username and closes the window
        def submit():
            username = name.get()

            if username:
                self.username = username
                name_window.destroy()

            else:
                print("Error: Username cannot be empty.")

        name_entry.bind("<Return>", lambda event: submit())  # Bind Enter key to submit
        submit_button = tk.Button(name_window, text="Submit", command=submit)
        submit_button.pack(pady=10)

        self.master.wait_window(name_window)  # Wait for the name window to close


    def read_socket(self):
        host = '127.0.0.1'  # Replace with your host
        port = 5000        # Replace with your port

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))

            # Send the username to the server
            self.socket.sendall(self.username.encode())

            # Receive messages from the server
            while self.running:
                data = self.socket.recv(1024)
                if not data:
                    break
                self.data_queue.put(data.decode())

        except socket.error as e:
            if e.errno == 10054:  # If server is suddenly disconnected
                self.data_queue.put("Server Disconnected. Closing app in 5 seconds.")
                self.master.after(5000, self.close)  # Close the app in 5 seconds. This is the first time I've used the after() method
            else:
                self.data_queue.put(f"Error: {e}")
        finally:
            if self.socket:
                self.socket.close()

    def setup_gui(self):
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, height=15)
        self.chat_display.pack(padx=10, pady=5, expand=True, fill='both')
        self.chat_display.config(state=tk.DISABLED)  # Chat should be read-only

        # Input area
        input_area = tk.Frame(self.master)
        input_area.pack(padx=10, pady=5, fill=tk.X)

        # Message entry field
        self.message_entry = tk.Entry(input_area)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message()) # Bind Enter key to send message

        # Send button
        self.send_button = tk.Button(input_area, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)


    def update_gui(self):
        try:
            data = self.data_queue.get_nowait() 
            self.label_text.set(data)
            self.update_chat(data) 
        except queue.Empty:
            pass  # No data yet, ignore
        if self.running:
            self.master.after(100, self.update_gui) # Check every 100 ms

    def update_chat(self, message):
        """ Updates the chat display with the new message """
        self.chat_display.config(state=tk.NORMAL)  # Enable editing
        self.chat_display.insert(tk.END, message + "\n")  # Add the new message
        self.chat_display.config(state=tk.DISABLED) # Disable editing 
        self.chat_display.see(tk.END)
        
    def send_message(self):
        """ Sends the user's message to the server """
        message = self.message_entry.get()  # Get the text from the input field
        if message.strip():  # Check if the message is not empty
            formatted_message = f"{self.username}: {message}"
            try:
                self.socket.sendall(formatted_message.encode())  # Send to server
                self.update_chat(formatted_message)  # Update chat display
                self.message_entry.delete(0, tk.END)  # Clear the input field
            except Exception as e:
                self.update_chat(f"Error sending message: {e}")
                print(f"Error sending: {e}")

    def close(self):
        self.running = False
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


''' 
Levi Klamer & Ryan Langren
Total Time Spent: 5 hours
Main Issues: 
Keyboard Interrupt doesn't work in the server
No testing has been done outside local

References:
https://docs.python.org/3/library/tk.html
https://docs.python.org/3/library/socket.html
https://www.askpython.com/python-modules/tkinter/tkinter-padding-tutorial                         -- Tkinter formatting via padding
https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/                             -- Using lambda in GUI programs in Python
https://stackoverflow.com/questions/16996432/how-do-i-bind-the-enter-key-to-a-function-in-tkinter -- Binding Enter key to a function in Tkinter

'''