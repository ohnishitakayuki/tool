import tkinter as tk

from app.pos_spc_app import PosSpcApp


if __name__ == '__main__':
    root = tk.Tk()
    PosSpcApp(master=root)
    root.mainloop()
