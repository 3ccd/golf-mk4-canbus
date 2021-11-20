import tkinter as tk
from tkinter import ttk


class DataTable(ttk.Treeview):

    def __init__(self, master, columns, height):
        super().__init__(master, columns=columns, height=height)
        self.dict = {}

    def all_delete(self):
        for i in self.get_children():
            self.delete(i)

    def data_update(self, can_data):
        if can_data is None:
            return

        self.all_delete()
        count = 0
        for key in can_data:
            can_data_bytes = can_data[key].encode
            self.insert(parent='', index='end', iid=count, values=[key, can_data[key]])
            count += 1


class Gui(tk.Tk):

    def __init__(self, window_size, title, conn):
        super().__init__()
        self.conn = conn
        self.callback = None

        self.geometry(window_size)
        self.title(title)

        self.table = DataTable(self, columns=['rid', 'data'], height=30)
        self.table.column('#0', width=50)
        self.table.column('rid', width=100)
        self.table.column('data', width=500)
        self.table.heading('rid', text='ReceiveID')
        self.table.heading('data', text='Data')
        self.table.pack()

        self.label = ttk.Label(self, text='textLabel')
        self.label.pack()

        open_button = ttk.Button(self, text='Open', command=self.conn.open)
        open_button.pack()
        start_button = ttk.Button(self, text='Start', command=self.start)
        start_button.pack()

    def get_table(self):
        return self.table

    def start(self):
        self.conn.start()
        self.update()

    def edit_text(self, text):
        self.label.configure(text=text)

    def set_callback(self, callback):
        self.callback = callback

    def update(self):
        self.callback()
        self.after(500, self.update)

    def show(self):
        self.mainloop()
