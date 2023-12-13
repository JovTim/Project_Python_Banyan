import tkinter as tk

class NewWindow(tk.Toplevel):
    def __init__(self, master, text):
        super().__init__(master)
        self.title(text)
        self.geometry("500x600")

        self.new_window_widgets()
    

    def new_window_widgets(self):
        bid_button = tk.Button(self, text="Bid", width=10)
        bid_button.place(x=10, y=10)

        sell_button = tk.Button(self, text="Sell", width=10)
        sell_button.place(x=100, y=10)

        bidding_label = tk.Label(self, text="Item for BIDDING", height=9)
        bidding_label.pack()
        listbox = tk.Listbox(
            self,
            height=6,
            width=15,
            bg="white",
            activestyle="dotbox",
            font="Helvetica",
            fg="black"
        )
        listbox.place(x=10, y=80, width=480)

        selling_label = tk.Label(self, text="Item you are SELLING")
        selling_label.place(x=190, y=220)
        listbox2 = tk.Listbox(
            self,
            height=6,
            width=15,
            bg="white",
            activestyle="dotbox",
            font="Helvetica",
            fg="black"
        )
        listbox2.place(x=10, y=240, width=480)

        highest_label = tk.Label(self, text="HIGHEST bidder")
        highest_label.place(x=190, y=390)
        listbox3 = tk.Listbox(
            self,
            height=6,
            width=15,
            bg="white",
            activestyle="dotbox",
            font="Helvetica",
            fg="black"
        )
        listbox3.place(x=10, y=410, width=480)


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ENTER YOUR NAME")
        self.root.geometry("400x150")

        self.create_widgets()

    def create_widgets(self):
        self.name_entry = tk.Entry(self.root, width=45)
        self.name_entry.place(x=10, y=30)

        submit_button = tk.Button(self.root, text="Accept", command=self.on_submit, width=10)
        submit_button.place(x=300, y=30)

    def on_submit(self):
        input_text = self.name_entry.get()
        if input_text:
            self.root.withdraw()
            new_window = NewWindow(self.root, input_text)
            new_window.protocol("WM_DELETE_WINDOW", self.on_new_window_close)
    
    def on_new_window_close(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

