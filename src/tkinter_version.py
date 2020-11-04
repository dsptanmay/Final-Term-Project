import tkinter as tk



class MainWindow:
    def __init__(self, master: tk.Tk):
        self.master = master


root = tk.Tk()

app=MainWindow(root)
root.mainloop()

