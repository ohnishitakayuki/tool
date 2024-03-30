import tkinter as tk

from app.cd_fft_app import CdFftApp


if __name__ == '__main__':
    root = tk.Tk()
    CdFftApp(master=root)
    root.mainloop()
