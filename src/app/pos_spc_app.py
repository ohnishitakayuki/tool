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
from analyzer.pos_spc_calc import PosSpcCalc


class PosSpcApp(tk.Frame):
    folder_name = 'pos_spc_app_folder'

    tool_title = "IPRO8 SPC解析ツール"
    release_date = "2023/10/16"
    version = "0.1"
    c_year = 2023
    maker_name = "NuFlare Technology Inc."

    # すでにグラフを作成したかの確認用
    is_graph = False
    last_path = ''

    # 設定ファイル
    p_config = Path(f'{os.path.dirname(__file__)}/{folder_name}/setting.ini')
    p_manual = Path(f'{os.path.dirname(__file__)}/{folder_name}/manual.txt')

    # 検索キーワード。変えることが多ければ、設定に入れる予定。
    search_baseline = '15x15_SPC_swath_Array*lms'
    search_word = '*15x15_SPC_swath_Array*lms'

    def __init__(self, master):
        super().__init__(master)
        # configファイル読み込み
        if not(self.p_config.exists()):
            messagebox.showerror("Error", "No settings.ini!!")
            sys.exit()

        self.pack()
        self.master.title(self.tool_title)
        self.master.geometry('800x600')

        # メニューバー
        menubar = tk.Menu(self)

        menu_file = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="ファイル", menu=menu_file)
        menu_file.add_command(label='Baselineフォルダパス設定', command=lambda: self.load_data(self.entry_baseline))
        menu_file.add_command(label='Dataフォルダパス設定', command=lambda: self.load_data(self.entry_data))
        menu_file.add_command(label='解析開始', command=self.menu_file_analysis)
        menu_file.add_separator()
        menu_file.add_command(label='再解析', command=self.menu_re_analysis)
        menu_file.add_command(label='すべてのデータを保存', command=lambda: self.menu_file_make_csv(data_type='all'))
        menu_file.add_command(label='最大値のデータのみ保存', command=lambda: self.menu_file_make_csv(data_type='ave'))
        menu_file.add_command(label='グラフを保存', command=self.menu_file_make_graph)
        menu_file.add_separator()
        menu_file.add_command(label='ネットグラフを保存', command=self.menu_file_make_netgraph)
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
        self.menu_right.add_command(label='すべてのデータを保存', command=lambda: self.menu_file_make_csv(data_type='all'))
        self.menu_right.add_command(label='最大値のデータのみ保存', command=lambda: self.menu_file_make_csv(data_type='ave'))
        self.menu_right.add_command(label='グラフを保存', command=self.menu_file_make_graph)
        self.menu_right.add_command(label='ネットグラフを保存', command=self.menu_file_make_netgraph)

        self.master.bind('<Button-3>', self.show_menu)

        # パス入力 baseline
        self.Frame_baseline = tk.Frame(self.master)
        self.Frame_baseline.pack(side=tk.TOP)

        self.label_baseline = tk.Label(self.Frame_baseline, text='Baselineフォルダパス', width=15)
        self.label_baseline.pack(side=tk.LEFT)

        self.entry_baseline = tk.Entry(self.Frame_baseline, width=50)
        self.entry_baseline.pack(side=tk.LEFT)

        self.Button_baseline = tk.Button(self.Frame_baseline, text='フォルダ選択',
                                         command=lambda: self.load_data(self.entry_baseline))
        self.Button_baseline.pack(side=tk.LEFT)

        # パス入力 data
        self.Frame_data = tk.Frame(self.master)
        self.Frame_data.pack(side=tk.TOP)

        self.label_data = tk.Label(self.Frame_data, text='Dataフォルダパス', width=15)
        self.label_data.pack(side=tk.LEFT)

        self.entry_data = tk.Entry(self.Frame_data, width=50)
        self.entry_data.pack(side=tk.LEFT)

        self.Button_data = tk.Button(self.Frame_data, text='フォルダ選択',
                                         command=lambda: self.load_data(self.entry_data))
        self.Button_data.pack(side=tk.LEFT)

        # 解析実行ボタン
        self.Frame_analysis = tk.Frame(self.master)
        self.Frame_analysis.pack(side=tk.TOP)

        self.Button_analysis = tk.Button(self.Frame_analysis, text='解析開始',
                                     command=lambda: self.menu_file_analysis())
        self.Button_analysis.pack(side=tk.LEFT)


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

        # 補正
        self.r_correction = tk.IntVar()
        self.r_correction.set(v['sw'])
        self.l_correction = ttk.Label(sub_frame, text='補正')
        self.l_correction.grid(column=0, row=1)
        self.r_correction1 = tk.Radiobutton(sub_frame, text='補正無し', variable=self.r_correction, value='0')
        self.r_correction1.grid(column=1, row=1)
        self.r_correction2 = tk.Radiobutton(sub_frame, text='Shift+Rot', variable=self.r_correction, value='1')
        self.r_correction2.grid(column=2, row=1)
        self.r_correction3 = tk.Radiobutton(sub_frame, text='一次補正', variable=self.r_correction, value='2')
        self.r_correction3.grid(column=3, row=1)

        # 解析最大数
        self.l_max_meas = ttk.Label(sub_frame, text='解析する最大データ数')
        self.l_max_meas.grid(column=0, row=2)
        self.r_max_meas = tk.IntVar()
        self.r_max_meas.set(v['max_meas'])
        self.r_max_meas = tk.Entry(sub_frame, textvariable=self.r_max_meas, width=4, justify=tk.CENTER)
        self.r_max_meas.grid(column=1, row=2)

        # ネットグラフピッチ
        self.l_netgraph_pitch = ttk.Label(sub_frame, text='ネットグラフ Pitch size [nm]')
        self.l_netgraph_pitch.grid(column=0, row=3)
        self.r_netgraph_pitch = tk.DoubleVar()
        self.r_netgraph_pitch.set(v['netgraph_pitch'])
        self.r_netgraph_pitch = tk.Entry(sub_frame, textvariable=self.r_netgraph_pitch, width=4, justify=tk.CENTER)
        self.r_netgraph_pitch.grid(column=1, row=3)

        # 初期値設定
        self.default_button = tk.Button(sub_frame, text="初期値設定", command=self.sub_default)
        self.default_button.grid(column=1, row=4)

        # 保存
        self.save_button = tk.Button(sub_frame, text="保存", command=self.sub_save)
        self.save_button.grid(column=2, row=4)

    def load_data(self, entry):
        entry.delete(0, tk.END)
        file_path = tk.filedialog.askdirectory(
                            title='フォルダ選択',
                            initialdir='./',
                        )
        entry.insert(tk.END, file_path)

    def show_menu(self, e):
        self.menu_right.post(e.x_root, e.y_root)

    def menu_file_analysis(self):
        p_baseline = Path(self.entry_baseline.get())
        p_data = Path(self.entry_data.get())
        if str(p_baseline) == '.' or not(p_baseline.exists()):
            messagebox.showwarning('注意', 'baselineのパスは存在しません。')
            return
        if str(p_data) == '.' or not(p_data.exists()):
            messagebox.showwarning('注意', 'dataのパスは存在しません。')
            return
        self.p_baseline = p_baseline
        self.p_data = p_data
        self._analysis(p_baseline, p_data)

    def _analysis(self, p_baseline, p_data):
        self.statusbar.configure(text='解析中...')
        self.statusbar.update()
        t = threading.Thread(target=self._make_graph(p_baseline, p_data))
        t.start()

    def menu_file_make_csv(self, data_type):
        if not self.is_graph:
            messagebox.showwarning('注意', 'まだグラフが生成されていません。')
            return
        if data_type == 'all':
            window_title = 'すべてのデータを保存'
        elif data_type == 'ave':
            window_title = '最大値のデータのみ保存'
        filename = filedialog.asksaveasfilename(
            title=window_title,
            initialdir='./',
            filetypes=[("CSV", ".csv")],
        )
        if not filename:
            return
        if data_type == 'all':
            df = self.v.df_all
        elif data_type == 'ave':
            df = self.v.df_ave
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

    def menu_file_make_netgraph(self):
        v = self._read_config()
        netgraph_pitch = float(v['netgraph_pitch'])
        if not self.is_graph:
            messagebox.showwarning('注意', 'まだグラフが生成されていません。')
            return
        filename = filedialog.askdirectory(
            title='ネットグラフを保存',
            initialdir='./',
        )
        if not filename:
            return
        self.v.netgraph(filename, pitch_size=netgraph_pitch)

    def sub_save(self):
        if not self.r_max_meas.get().isdigit():
            messagebox.showerror("入力エラー", "解析する最大データ数に数値以外のものが入っています。")
            return
        elif int(self.r_max_meas.get()) == 0:
            messagebox.showerror("入力エラー", "解析する最大データ数に0が入っています。")
            return
        if not(self._is_num(self.r_netgraph_pitch.get())):
            messagebox.showerror("入力エラー", "ネットグラフPitch sizeに数値以外のものが入っています。")
            return
        elif float(self.r_netgraph_pitch.get()) <= 0:
            messagebox.showerror("入力エラー", "ネットグラフPitch sizeに0以下の値が入っています。")
            return
        self.config_ini.set('preference', 'sw', str(self.r_correction.get()))
        self.config_ini.set('preference', 'max_meas', str(self.r_max_meas.get()))
        self.config_ini.set('preference', 'netgraph_pitch', str(self.r_netgraph_pitch.get()))
        with open(self.p_config, "w") as file:
            self.config_ini.write(file)
        self.sub_window.destroy()

    def sub_default(self):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.read(self.p_config)
        default = {}
        for k, value in self.config_ini['default'].items():
            default[k] = value

        self.r_correction.set(default['sw'])
        self.r_max_meas.delete(0, tk.END)
        self.r_max_meas.insert(tk.END, default['max_meas'])


    def menu_re_analysis(self):
        if not self.is_graph:
            messagebox.showwarning('注意', 'まだ解析データを選択していません。')
            return
        self._analysis(self.p_baseline, self.p_data)

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

    def _make_graph(self, p_baseline, p_data):
        # Config初期値設定
        v = self._read_config()
        sw = int(v['sw'])
        max_meas = int(v['max_meas'])
        netgraph_pitch = float(v['netgraph_pitch'])
        try:
            print(p_baseline)
            self.v = PosSpcCalc(p_baseline, p_data, self.search_baseline, self.search_word,
                                sw=sw, max_meas=max_meas)
        except FileNotFoundError:
            messagebox.showerror('エラー', '解析ファイルが見つかりません。')
            return
        except KeyError:
            messagebox.showerror('エラー', 'データ解析ができません。フォルダ選択が間違っている可能性があります。')
            return
        fig, ax = self.v.graph()
        # すでにグラフを描いたことがあるか確認。ある場合は一度初期化。
        if self.is_graph:
            self.canvas.get_tk_widget().destroy()

        # ステータスバー表示
        m_sw = {0: '補正無し', 1: 'Shift+Rotation補正', 2: '一次補正'}
        self.statusbar['text'] = f'{m_sw[sw]}　最大データ数 {max_meas}個'

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

    def _is_num(self, s):
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True


if __name__ == '__main__':
    root = tk.Tk()
    PosSpcApp(master=root)
    root.mainloop()



