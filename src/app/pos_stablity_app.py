import os
import sys
import subprocess

import matplotlib.pyplot as plt
from pathlib import Path
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
from analyzer.pos_stability_calc import PosStabilityCalc


class PosStabilityApp(tk.Frame):
    p_config = Path(f'{os.path.dirname(__file__)}/pos_stability_app_folder/setting.ini')
    p_manual = Path(f'{os.path.dirname(__file__)}/pos_stability_app_folder/manual.txt')
    tool_title = "ポジション安定性確認ツール"
    release_date = "2023/9/25"
    version = "0.1"
    c_year = 2023
    maker_name = "NuFlare Technology Inc."

    # すでにグラフを作成したかの確認用
    is_graph = False
    last_path = ''

    # パラメータデフォルト値
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

    def show_menu(self, e):
        self.menu_right.post(e.x_root, e.y_root)

    def menu_file_open_click(self, event=None):
        filename = filedialog.askdirectory(
            title='lmsファイルを開く',
            initialdir='./'
        )
        if not filename:
            return
        self.last_path = filename
        self._analysis(filename)

    def _analysis(self, filename):
        self.statusbar.configure(text='解析中...')
        self.statusbar.update()
        t = threading.Thread(target=self._make_graph(filename))
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
        df = self.v.df_stab
        p = Path(filename)
        if p.suffix != '.csv':
            p = str(p) + '.csv'
        df.to_csv(p, index=None)

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

    def menu_graph_preference(self):
        v = self._read_config()

        self.sub_window = tk.Toplevel(self)
        self.sub_window.title("解析設定")
        self.sub_window.grab_set()
        self.sub_window.focus_set()
        self.sub_window.transient(self.master)

        sub_frame = ttk.Frame(self.sub_window)
        sub_frame.grid(column=0, row=0, padx=5, pady=10)

        # ロードごとの解析設定
        self.r_same_load_value = tk.BooleanVar()
        self.r_same_load_value.set(v['same_load'])
        self.l_same_load = ttk.Label(sub_frame, text='ロードごとの解析')
        self.l_same_load.grid(column=0, row=0)
        self.r_same_load1 = tk.Radiobutton(sub_frame, text='ロードごと', variable=self.r_same_load_value, value=True,
                                           command=self._switch_off)
        self.r_same_load1.grid(column=1, row=0)
        self.r_same_load2 = tk.Radiobutton(sub_frame, text='ロード無視', variable=self.r_same_load_value, value=False,
                                           command=self._switch_on)
        self.r_same_load2.grid(column=2, row=0)

        # 平均数
        self.l_average = ttk.Label(sub_frame, text='平均測定数')
        self.l_average.grid(column=0, row=1)
        self.r_average = tk.IntVar()
        self.r_average.set(v['average'])
        if v['same_load'] == 'True':
            a_status = tk.DISABLED
        else:
            a_status = tk.NORMAL
        self.r_average = tk.Entry(sub_frame, textvariable=self.r_average, width=4, justify=tk.CENTER, state=a_status)
        self.r_average.grid(column=1, row=1)

        # 補正
        self.r_correction_value = tk.IntVar()
        self.r_correction_value.set(v['correction'])
        self.l_correction = ttk.Label(sub_frame, text='補正')
        self.l_correction.grid(column=0, row=2)
        self.r_correction1 = tk.Radiobutton(sub_frame, text='補正無し', variable=self.r_correction_value, value='0')
        self.r_correction1.grid(column=1, row=2)
        self.r_correction2 = tk.Radiobutton(sub_frame, text='Shift+Rot', variable=self.r_correction_value, value='1')
        self.r_correction2.grid(column=2, row=2)
        self.r_correction3 = tk.Radiobutton(sub_frame, text='一次補正', variable=self.r_correction_value, value='2')
        self.r_correction3.grid(column=3, row=2)

        # 初期値設定
        self.default_button = tk.Button(sub_frame, text="初期値設定", command=self.sub_default)
        self.default_button.grid(column=1, row=3)

        # 保存
        self.save_button = tk.Button(sub_frame, text="保存", command=self.sub_save)
        self.save_button.grid(column=2, row=3)

    def sub_save(self):
        if not self.r_average.get().isdigit():
            messagebox.showerror("入力エラー", "平均値に数値以外のものが入っています。")
            return
        self.config_ini.set('preference', 'same_load', str(self.r_same_load_value.get()))
        self.config_ini.set('preference', 'average', self.r_average.get())
        self.config_ini.set('preference', 'correction', str(self.r_correction_value.get()))
        with open(f"{os.path.dirname(__file__)}/pos_stability_app_folder/setting.ini", "w") as file:
            self.config_ini.write(file)
        self.sub_window.destroy()

    def sub_default(self):
        self.r_same_load_value.set(self.default_load)
        self.r_average.delete(0, tk.END)
        self.r_average.insert(tk.END, self.default_average)
        self.r_correction_value.set(self.default_correction)
        if self.default_load == True:
            self.r_average.config(state=tk.DISABLED)
        else:
            self.r_average.config(state=tk.NORMAL)

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

    def _make_graph(self, filename):
        # Config読み込み。すべて文字列で読み込むので、
        # 数字系はint、boolean系はbool変換を忘れずに行うこと。
        v = self._read_config()
        if v['same_load'] == 'True':
            same_load = True
        else:
            same_load = False
        average = int(v['average'])
        correction = int(v['correction'])

        try:
            self.v = PosStabilityCalc(filename, same_load=same_load, average_num=average, sw=correction)
        except FileNotFoundError:
            messagebox.showerror('エラー', '解析ファイルが見つかりません。')
            return
        fig, ax = self.v.graph()
        # すでにグラフを描いたことがあるか確認。ある場合は一度初期化。
        if self.is_graph:
            self.canvas.get_tk_widget().destroy()

        self.statusbar['text'] = filename
        self.canvas = FigureCanvasTkAgg(fig, self.Frame1)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot1 = ax
        self.is_graph = True

    def _read_config(self):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.read(self.p_config)
        v = {
            'same_load':  self.config_ini['preference']['same_load'],
            'average': self.config_ini['preference']['average'],
            'correction': self.config_ini['preference']['correction'],
        }
        return v

    # averageのウィジェット動的操作
    def _switch_on(self):
        self.r_average.config(state=tk.NORMAL)

    def _switch_off(self):
        self.r_average.config(state=tk.DISABLED)


if __name__ == '__main__':
    root = tk.Tk()
    PosStabilityApp(master=root)
    root.mainloop()


