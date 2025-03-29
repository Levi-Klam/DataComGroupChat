import tkinter as tk
import threading
import socket
import queue

class App:
    def __init__(self, master):
        self.master = master
        master.title("Socket Reader")

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

        self.update_gui()

    def get_username(self):
        name_window = tk.Toplevel(self.master)
        name_window.title("Enter a Username")
        name_window.geometry("300x100")
        name_window.transient(self.master)  # Makes it the secondary window
        name_window.grab_set()  # Can't interact with the main window until this one is closed

        tk.Label(name_window, text="Enter your username:").pack(pady=10) 

        name = tk.StringVar() 
        name_entry = tk.Entry(name_window, textvariable=name)
        name_entry.pack(pady=10)
        name_entry.focus_set()

        def submit():
            username = name.get()

            if username:
                self.username = username
                print(f"Username set to: {self.username}")  
                name_window.destroy()
            else:
                tk.messagebox.showerror("Error", "Username cannot be empty.")

        name_entry.bind("<Return>", lambda event: submit())  # Bind Enter key to submit
        submit_button = tk.Button(name_window, text="Submit", command=submit)
        submit_button.pack(pady=10)

        self.master.wait_window(name_window)  # Wait for the name window to close



    def read_socket(self):
        host = '127.0.0.1'  # Replace with your host
        port = 5000        # Replace with your port

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                while self.running:
                    data = s.recv(1024)
                    if not data:
                        break
                    self.data_queue.put(data.decode())
        except Exception as e:
             self.data_queue.put(f"Error: {e}")

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
        pass
        

    def close(self):
        self.running = False
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400") # Set the window size
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.close) # Handle window close event
    root.mainloop()


''' 
References:
https://docs.python.org/3/library/tk.html
https://docs.python.org/3/library/socket.html
https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/                             -- Using lambda in GUI programs in Python
https://stackoverflow.com/questions/16996432/how-do-i-bind-the-enter-key-to-a-function-in-tkinter -- Binding Enter key to a function in Tkinter

'''