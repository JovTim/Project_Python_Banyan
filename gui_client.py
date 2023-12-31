import tkinter as tk
import socket
import pickle
import threading
import time

class NewWindow(tk.Toplevel):
    def __init__(self, master, text):
        super().__init__(master)
        self.title(text)
        self.client_name = text
        self.geometry("500x600")
        self.bidding = {"Snake": 100, "Bottle": 50}
        self.selling = {}
        self.higher = {}

        self.countdown_var = tk.StringVar()
        self.countdown_time = 0
        self.timer_started = False
        self.new_window_widgets()

        receive_thread = threading.Thread(target=self.receive_countdown_time)
        receive_thread.start()

    def new_window_widgets(self):
        self.bid_button = tk.Button(self, text="Bid", state='disabled', width=10, command=self.bid_action)
        self.bid_button.place(x=10, y=10)

        self.sell_button = tk.Button(self, text="Sell", state='disabled', width=10, command=self.selling_window)
        self.sell_button.place(x=100, y=10)

        bidding_label = tk.Label(self, text="Item for BIDDING", height=9)
        bidding_label.pack()

        countdown_text = tk.Label(self, text="Countdown: ")
        countdown_text.place(x=320, y=10)
        countdown_label = tk.Label(self, textvariable=self.countdown_var)
        countdown_label.place(x=400, y=10)

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

    def start_countdown(self, countdown_time):
        self.countdown_time = countdown_time
        self.timer_started = True
        self.update_ui()

    def receive_countdown_time(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('IP', port)) #LAGAY MO YUNG PORT AND IP MO. DAPAT SAME SIYA SA CLIENT
        server.listen(1)

        while True:
            conn, addr = server.accept()
            data = conn.recv(4096)
            countdown_time = pickle.loads(data)
            conn.close()

            self.start_countdown(countdown_time)

    def update_ui(self):
        if self.timer_started and self.countdown_time >= 0:  # Ensuring countdown stops at 0
            self.bid_button.config(state='normal')
            self.sell_button.config(state='normal')
            if self.countdown_time > 0:  # Decrement countdown when greater than 0
                self.countdown_time -= 1
            self.countdown_var.set(self.countdown_time)
            self.after(1000, self.update_ui)  # Update every 1 second

            if self.countdown_time == 0:  # Disable buttons when countdown reaches 0
                self.timer_started = False
                self.bid_button.config(state='disabled')
                self.sell_button.config(state='disabled')
        else:
            self.bid_button.config(state='disabled')
            self.sell_button.config(state='disabled')
#-------------------------------------------  
    def bid_action(self):
        index = self.listbox.curselection()
        if index:
            selected_item = self.listbox.get(index)
            item_name = selected_item.split(" ---- ")[0]
            self.bidding_window_lambda = lambda item=item_name: self.bidding_window(item)
            self.bidding_window_lambda()

    def bidding_window(self, item_name):
        new_window = tk.Toplevel(self)
        new_window.title("BIDDING") 
        new_window.geometry("450x100")

        item_price_text = tk.Label(new_window, text=f"Bid Price for {item_name}:")
        item_price_text.pack()
        item_price = tk.Entry(new_window)
        item_price.pack()

        def bidding_closing_window():
            entered_price = float(item_price.get())
            if entered_price > self.bidding[item_name]:
                print("Bid accepted!") #sample lang
                new_window.destroy()
            else:
                error_label = tk.Label(new_window, text="Bid price should be higher than the item price.")
                error_label.pack()
            
        bid_closing_window = tk.Button(new_window, text="Accept", command=bidding_closing_window)
        bid_closing_window.place(x=200, y=60)


    
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

