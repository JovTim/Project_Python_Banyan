import tkinter as tk

class NewWindow(tk.Toplevel):
    def __init__(self, master, text):
        super().__init__(master)
        self.title(text)
        self.client_name = text
        self.geometry("500x600")
        self.bidding = {"Snake": 100, "Bottle": 50}
        self.selling = {}

        self.new_window_widgets()
    

    def new_window_widgets(self):
        self.bid_button = tk.Button(self, text="Bid", width=10, command = lambda: (self.bid_action(), self.bidding_window()))
        self.bid_button.place(x=10, y=10)

        sell_button = tk.Button(self, text="Sell", width=10, command=self.selling_window)
        sell_button.place(x=100, y=10)

        bidding_label = tk.Label(self, text="Item for BIDDING", height=9)
        bidding_label.pack()
        self.listbox = tk.Listbox(
            self,
            height=6,
            width=15,
            bg="white",
            activestyle="dotbox",
            font="Helvetica",
            fg="black"
        )
        self.listbox.place(x=10, y=80, width=480)

        for key, value in self.bidding.items():
            self.listbox.insert(tk.END, f"{key} ---- {value}")

        selling_label = tk.Label(self, text="Item you are SELLING")
        selling_label.place(x=190, y=220)
        self.listbox2 = tk.Listbox(
            self,
            height=6,
            width=15,
            bg="white",
            activestyle="dotbox",
            font="Helvetica",
            fg="black"
        )
        self.listbox2.place(x=10, y=240, width=480)

        self.update_listbox2()



        highest_label = tk.Label(self, text="HIGHEST bidder")
        highest_label.place(x=190, y=390)
        self.listbox3 = tk.Listbox(
            self,
            height=6,
            width=15,
            bg="white",
            activestyle="dotbox",
            font="Helvetica",
            fg="black"
        )
        self.listbox3.place(x=10, y=410, width=480)
    
    
    def update_listbox2(self):
        self.listbox2.delete(0, tk.END)
        for key, value in self.selling.items():
            self.listbox2.insert(tk.END, f"{key} ---- Php {value}")
    
    def bid_action(self):
        index = self.listbox.curselection()
        if index:
            selected_item = self.listbox.get(index)
            print(f"Bidding action for: {selected_item}")
            
    def bidding_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("BIDDING")
        new_window.geometry("450x100")

        item_price_text = tk.Label(new_window, text="Price: ")
        item_price_text.pack()
        item_price = tk.Entry(new_window)
        item_price.pack()

        def bidding_closing_window():
            pass
            
        bid_closing_window = tk.Button(new_window, text="Accept")
        bid_closing_window.place(x=200, y=50)


    
    def selling_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("SELLING")
        new_window.geometry("450x100")

        item_selling_text = tk.Label(new_window, text="Items: ")
        item_selling_text.place(x=10, y=10)
        item_selling = tk.Entry(new_window)
        item_selling.place(x=50, y=10)

        item_price_text = tk.Label(new_window, text="Price: ")
        item_price_text.place(x=250, y=10)
        item_price = tk.Entry(new_window)
        item_price.place(x=290, y=10)

        def selling_window_close():
            item_input = item_selling.get()
            item_price_inp = item_price.get()

            if item_input and item_price_inp:
                self.selling[item_input] = item_price_inp
                self.update_listbox2()

            new_window.destroy()
    
        sell_window_sub_button = tk.Button(new_window, text="Accept", command=selling_window_close)
        sell_window_sub_button.place(x=200, y=50)



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

