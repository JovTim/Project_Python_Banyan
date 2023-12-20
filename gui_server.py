import tkinter as tk
import socket
import pickle


class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SERVER")
        self.root.geometry("400x550")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="ACTIONS")
        self.label.pack()

        self.listbox = tk.Listbox(
            self.root,
            height=24,
            width=15,
            bg="white",
            activestyle="dotbox",
            font="Helvetica",
            fg="black"
        )
        self.listbox.pack(fill=tk.X)
        self.timer_label = tk.Label(self.root, text="Countdown (Seconds)")
        self.timer_label.place(x=30, y=515)
        self.timer_entry = tk.Entry(self.root, width=10)
        self.timer_entry.place(x=165,y=515)

        self.populate_listbox()

    def populate_listbox(self):
        pass
        #food_items = ["Nachos", "Sandwich"]
        #for item in food_items:
        #    self.listbox.insert(tk.END, item)

    def start_button(self):
        countdown_time = int(self.timer_entry.get())

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 54136)) #LAGAY MO YUNG PORT AND IP MO. DAPAT SAME SIYA SA CLIENT

        data = pickle.dumps(countdown_time)
        s.sendall(data)

        s.close()

    
    def close_button(self):
        self.root.destroy()
    
    


def main():
    root = tk.Tk()
    app = ServerApp(root)
    start_button = tk.Button(root, text="Start", command=app.start_button, width=8, height=1)
    start_button.pack()
    start_button.place(x=250, y=515)
    close_button = tk.Button(root, text="Close", command=app.close_button, width=8, height=1)
    close_button.pack()
    close_button.place(x=320, y=515)
    root.mainloop()

if __name__ == "__main__":
    main()
