import tkinter as tk
from tkinter import ttk


# class ChildWindow(tk.Toplevel):
#     def __init__(self, parent):
#         super().__init__(parent)

#         self.geometry('300x100')
#         self.title('Toplevel Window')

#         ttk.Button(self,
#                 text='Close',
#                 command=self.destroy).pack(expand=True)


class MainWindow (tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('720x480') 
        self.title('Change')
        self.colors = ["#E5E9EC","#DDCAD9","#7C616C"]
        style = ttk.Style(self)
        style.configure("primary.TFrame", background=self.colors[0])
        self.configure(background=self.colors[0])      
        self.selectionframe = ttk.Frame(self,width=900,height=50)
        self.selectionframe.pack(padx=5,pady=5,side="top",anchor='nw')
        self.fileselector = ttk.Entry(self.selectionframe,width=100,)
        self.fileselector.pack(ipady=5)

    # def open_window(self):
    #     window = MainWindow (self)
    #     window.grab_set()


if __name__ == "__main__":
    app = MainWindow ()
    app.mainloop()