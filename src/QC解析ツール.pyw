import tkinter as tk

from app.qc_app import QCApp


if __name__ == '__main__':
    root = tk.Tk()
    QCApp(master=root)
    root.mainloop()
