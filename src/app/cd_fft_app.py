import os
import sys
import subprocess


import matplotlib.pyplot as plt
from pathlib import Path
from distutils.util import strtobool
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import configparser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd_fft_calc import CdFftCalc



class CdFftApp(tk.Frame):
    folder_name = 'cd_fft_app_folder'

    tool_title = "Advantest エッジポジションFFTツール"
    release_date = "2023/10/5"
    version = "0.1"
    c_year = 2023
    maker_name = "NuFlare Technology Inc."

    # すでにグラフを作成したかの確認用
    is_graph = False
    last_path = ''

    # 設定ファイル
    p_config = Path(f'{os.path.dirname(__file__)}/{folder_name}/setting.ini')
    p_manual = Path(f'{os.path.dirname(__file__)}/{folder_name}/manual.txt')

    default_load = False
    default_average = 10
    default_correction = 1

    def __init__(self, master):
        super().__init__(master)
        # configファイル読み込み
        if not(self.p_config.exists()):
            messagebox.showerror("Error", "No settings.ini!!")
            sys.exit()

        self.pack()
        self.master.title(self.tool_title)
        self.master.geometry('600x500')

        # メニューバー
        menubar = tk.Menu(self)

        menu_file = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="ファイル", menu=menu_file)
        menu_file.add_command(label='ファイルを開く', command=self.menu_file_open_click)
        menu_file.add_separator()
        menu_file.add_command(label='再解析', command=self.menu_re_analysis)
        menu_file.add_command(label='データを保存', command=self.menu_file_make_csv)
        menu_file.add_command(label='グラフを保存', command=self.menu_file_make_graph)
        menu_file.add_separator()
        menu_file.add_command(label="終了", command=self.master.destroy)

        menu_preference = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="設定", menu=menu_preference)
        menu_preference.add_command(label='解析設定', command=self.menu_graph_preference)

        menu_preference = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="ヘルプ", menu=menu_preference)
        menu_preference.add_command(label='バージョン情報', command=self.menu_version)
        menu_preference.add_command(label='詳細情報', command=self.menu_manual)

        self.master.config(menu=menubar)

        # 右クリックメニュー
        self.menu_right = tk.Menu(self, tearoff=0)
        self.menu_right.add_command(label='再解析', command=self.menu_re_analysis)
        self.menu_right.add_command(label='データを保存', command=self.menu_file_make_csv)
        self.menu_right.add_command(label='グラフを保存', command=self.menu_file_make_graph)

        self.master.bind('<Button-3>', self.show_menu)

        # 本体
        self.Frame1 = tk.Frame(self.master)
        self.Frame1.pack(side=tk.TOP, fill=tk.X)

        # ステータスバー
        self.statusbar = tk.Label(self.master, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)


    def menu_graph_preference(self):
        v = self._read_config()

        self.sub_window = tk.Toplevel(self)
        self.sub_window.title("解析設定")
        self.sub_window.grab_set()
        self.sub_window.focus_set()
        self.sub_window.transient(self.master)

        sub_frame = ttk.Frame(self.sub_window)
        sub_frame.grid(column=0, row=0, padx=5, pady=10)

        # エッジタイプ
        self.r_edge_type = tk.StringVar()
        self.r_edge_type.set(v['edge_type'])
        self.l_edge_type = ttk.Label(sub_frame, text='FFT解析対象')
        self.l_edge_type.grid(column=0, row=0)
        self.r_edge_type1 = tk.Radiobutton(sub_frame, text='左エッジ', variable=self.r_edge_type, value='edge_left')
        self.r_edge_type1.grid(column=1, row=0)
        self.r_edge_type2 = tk.Radiobutton(sub_frame, text='右エッジ', variable=self.r_edge_type, value='edge_right')
        self.r_edge_type2.grid(column=2, row=0)
        self.r_edge_type3 = tk.Radiobutton(sub_frame, text='LWR', variable=self.r_edge_type, value='lwr')
        self.r_edge_type3.grid(column=3, row=0)

        # 平均するかどうか
        self.r_averaged = tk.BooleanVar()
        self.r_averaged.set(v['averaged'])
        self.l_averaged = ttk.Label(sub_frame, text='複数データ処理')
        self.l_averaged.grid(column=0, row=1)
        self.r_averaged1 = tk.Radiobutton(sub_frame, text='平均する', variable=self.r_averaged, value=True)
        self.r_averaged1.grid(column=1, row=1)
        self.r_averaged2 = tk.Radiobutton(sub_frame, text='個々に解析', variable=self.r_averaged, value=False)
        self.r_averaged2.grid(column=2, row=1)

        # ピクセル数 ON/OFF
        self.r_has_pixel = tk.BooleanVar()
        self.r_has_pixel.set(v['has_pixel'])
        self.l_has_pixel = ttk.Label(sub_frame, text='ピクセル数制限')
        self.l_has_pixel.grid(column=0, row=2)
        self.r_has_pixel1 = tk.Radiobutton(sub_frame, text='制限あり', variable=self.r_has_pixel, value=True,
                                           command=self._switch_on)
        self.r_has_pixel1.grid(column=1, row=2)
        self.r_has_pixel2 = tk.Radiobutton(sub_frame, text='制限無し', variable=self.r_has_pixel, value=False,
                                           command=self._switch_off)
        self.r_has_pixel2.grid(column=2, row=2)

        # ピクセル数
        self.l_pixel = ttk.Label(sub_frame, text='解析ピクセル数')
        self.l_pixel.grid(column=0, row=3)
        self.r_pixel = tk.IntVar()
        self.r_pixel.set(v['pixel'])
        if v['has_pixel'] == 'False':
            a_status = tk.DISABLED
        else:
            a_status = tk.NORMAL
        self.r_pixel = tk.Entry(sub_frame, textvariable=self.r_pixel, width=4, justify=tk.CENTER, state=a_status)
        self.r_pixel.grid(column=1, row=3)

        # 初期値設定
        self.default_button = tk.Button(sub_frame, text="初期値設定", command=self.sub_default)
        self.default_button.grid(column=1, row=4)

        # 保存
        self.save_button = tk.Button(sub_frame, text="保存", command=self.sub_save)
        self.save_button.grid(column=2, row=4)

    def show_menu(self, e):
        self.menu_right.post(e.x_root, e.y_root)

    def menu_file_open_click(self, event=None):
        filenames = filedialog.askopenfilenames(
            title='csvファイルを開く',
            initialdir='./'
        )
        if not filenames:
            return
        self.last_path = filenames
        self._analysis(filenames)

    def _analysis(self, filenames):
        self.statusbar.configure(text='解析中...')
        self.statusbar.update()
        t = threading.Thread(target=self._make_graph(filenames))
        t.start()

    def menu_file_make_csv(self):
        if not self.is_graph:
            messagebox.showwarning('注意', 'まだグラフが生成されていません。')
            return
        filename = filedialog.asksaveasfilename(
            title='データを保存',
            initialdir='./',
            filetypes=[("CSV", ".csv")],
        )
        if not filename:
            return
        df = self.v.df_all
        p = Path(filename)
        if p.suffix != '.csv':
            p = str(p) + '.csv'
        df.to_csv(p)

    def menu_file_make_graph(self):
        if not self.is_graph:
            messagebox.showwarning('注意', 'まだグラフが生成されていません。')
            return
        filename = filedialog.asksaveasfilename(
            title='グラフを保存',
            initialdir='./',
            filetypes=[("PNG", ".png")],
        )
        if not filename:
            return
        self.v.graph(filename)


    def sub_save(self):
        if not self.r_pixel.get().isdigit():
            messagebox.showerror("入力エラー", "pixelに数値以外のものが入っています。")
            return
        self.config_ini.set('preference', 'edge_type', str(self.r_edge_type.get()))
        self.config_ini.set('preference', 'averaged', str(self.r_averaged.get()))
        self.config_ini.set('preference', 'has_pixel', str(self.r_has_pixel.get()))
        self.config_ini.set('preference', 'pixel', self.r_pixel.get())
        with open(self.p_config, "w") as file:
            self.config_ini.write(file)
        self.sub_window.destroy()

    def sub_default(self):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.read(self.p_config)
        default = {}
        for k, value in self.config_ini['default'].items():
            default[k] = value

        self.r_edge_type.set(default['edge_type'])
        self.r_averaged.set(default['averaged'])
        self.r_has_pixel.set(default['has_pixel'])
        self.r_pixel.delete(0, tk.END)
        self.r_pixel.insert(tk.END, default['pixel'])
        if default['has_pixel'] == 'True':
            self.r_pixel.config(state=tk.NORMAL)
        else:
            self.r_pixel.config(state=tk.DISABLED)

    def menu_re_analysis(self):
        if not self.is_graph:
            messagebox.showwarning('注意', 'まだ解析データを選択していません。')
            return
        self._analysis(self.last_path)

    def menu_version(self):
        if self.c_year == datetime.now().year:
            c_year = self.c_year
        else:
            c_year = f'{self.c_year}-{datetime.now().year}'
        messagebox.showinfo('バージョン情報',  f'    {self.tool_title}\n' +
                                            f'    Version {self.version}\n'+
                                            f'    {self.release_date}\n' +
                                            f'    Copyright(C) {c_year}\n' +
                                            f'    {self.maker_name}')

    def menu_manual(self):
        subprocess.Popen(['start', '', self.p_manual], shell=True)

    def _make_graph(self, filenames):
        # Config初期値設定
        v = self._read_config()
        if v['has_pixel'] == 'False':
            pixel = None
        else:
            pixel = int(v['pixel'])
        edge_type = v['edge_type']
        averaged = strtobool(v['averaged'])
        try:
            self.v = CdFftCalc(filenames, edge_type, averaged, pixel)
        except FileNotFoundError:
            messagebox.showerror('エラー', '解析ファイルが見つかりません。')
            return
        fig, ax = self.v.graph()
        # すでにグラフを描いたことがあるか確認。ある場合は一度初期化。
        if self.is_graph:
            self.canvas.get_tk_widget().destroy()

        # ステータスバー表示
        m_edge_type = {'edge_left': '左エッジ', 'edge_right': '右エッジ', 'lwr': 'LWR'}
        m_averaged = {True: '平均グラフ', False: '個別グラフ'}
        if v['has_pixel']:
            m_pixel = 'pixel全部'
        else:
            m_pixel = pixel
        self.statusbar['text'] = f'データ {self.v.idx}個  {m_edge_type[edge_type]}  {m_averaged[averaged]}  {m_pixel}'

        self.canvas = FigureCanvasTkAgg(fig, self.Frame1)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot1 = ax
        self.is_graph = True

    def _read_config(self):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.read(self.p_config)
        v = {}
        for k, value in self.config_ini['preference'].items():
            v[k] = value
        return v

    # averageのウィジェット動的操作
    def _switch_on(self):
        self.r_pixel.config(state=tk.NORMAL)

    def _switch_off(self):
        self.r_pixel.config(state=tk.DISABLED)


if __name__ == '__main__':
    root = tk.Tk()
    CdFftApp(master=root)
    root.mainloop()



