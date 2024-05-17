import os
import sys

from pathlib import Path
import tkinter as tk
from tkinter import ttk
import configparser
import subprocess

from pprint import pprint

from tkinter import messagebox
from importlib import import_module

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from qc_auto import QCAnalysis


class QCApp(tk.Frame):
    folder_name = 'qc_app_folder'

    tool_title = "QC解析ツール"
    release_date = "2023/xx/xx"
    version = "0.1"
    c_year = 2023
    maker_name = "NuFlare Technology Inc."

    # 設定ファイル
    p_config = Path(f'{os.path.dirname(__file__)}/{folder_name}/')
    p_manual = Path(f'{os.path.dirname(__file__)}/{folder_name}/manual.txt')

    def __init__(self, master):
        super().__init__(master)
        list_machine = self.get_config_machine()

        self.pack()
        self.master.title(self.tool_title)
        self.master.geometry('700x500')

        # 解析実行ボタン
        self.Frame_analysis = tk.Frame(self.master)
        self.Frame_analysis.pack(side=tk.TOP)

        c_value = tk.StringVar()
        self.combobox = ttk.Combobox(self.master, textvariable=c_value, values=list_machine, style='office.TCombobox')
        self.combobox.bind('<<ComboboxSelected>>', lambda x: self.make_button(c_value.get()))
        self.combobox.pack()

        # ダミーヴィジェット
        self.Frame1 = tk.Frame(self.master)
        self.Frame1.pack(anchor=tk.CENTER)

        # ステータスバー
        self.statusbar = tk.Label(self.master, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def make_button(self, machine):
        # 装置のconfig取得
        list_items = self._read_config(machine)

        self.Frame1.destroy()
        self.Frame1 = tk.Frame(self.master)
        self.Frame1.pack(anchor=tk.CENTER)

        # ボタン作成部。複数個対応がexecでは無理だったので、頑張って個数分書く。
        num_items = len(list_items)

        # 1番目。i_numは0。
        if num_items == 0:
            return
        i_num = 0
        v = list_items[i_num]
        self.label_baseline1 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline1.grid(row=0, column=0, padx=3, pady=2)
        self.Button_baseline1 = tk.Button(self.Frame1, text='解析', command=lambda:self._calc_call(list_items[0]))
        self.Button_baseline1.grid(row=0, column=1, padx=3, pady=2)
        self.Button_baseline1 = tk.Button(self.Frame1, text='無視データ選択', command=lambda:self._ignore_call(list_items[0]))
        self.Button_baseline1.grid(row=0, column=2, padx=3, pady=2)
        self.Button_baseline1 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[0]))
        self.Button_baseline1.grid(row=0, column=3, padx=3, pady=2)
        self.Button_baseline1 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[0]))
        self.Button_baseline1.grid(row=0, column=4, padx=3, pady=2)

        # 2番目。i_numは1。
        if num_items == 1:
            return
        i_num = 1
        v = list_items[i_num]
        self.label_baseline2 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline2.grid(row=1, column=0, padx=3, pady=2)
        self.Button_baseline2 = tk.Button(self.Frame1, text='解析', command=lambda:self._calc_call(list_items[1]))
        self.Button_baseline2.grid(row=1, column=1, padx=3, pady=2)
        self.Button_baseline2 = tk.Button(self.Frame1, text='無視データ選択', command=lambda:self._ignore_call(list_items[1]))
        self.Button_baseline2.grid(row=1, column=2, padx=3, pady=2)
        self.Button_baseline2 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[1]))
        self.Button_baseline2.grid(row=1, column=3, padx=3, pady=2)
        self.Button_baseline2 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[1]))
        self.Button_baseline2.grid(row=1, column=4, padx=3, pady=2)

        # 3番目。i_numは2。
        if num_items == 2:
            return
        i_num = 2
        v = list_items[i_num]
        self.label_baseline3 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline3.grid(row=2, column=0, padx=3, pady=2)
        self.Button_baseline3 = tk.Button(self.Frame1, text='解析', command=lambda:self._calc_call(list_items[2]))
        self.Button_baseline3.grid(row=2, column=1, padx=3, pady=2)
        self.Button_baseline3 = tk.Button(self.Frame1, text='無視データ選択', command=lambda:self._ignore_call(list_items[2]))
        self.Button_baseline3.grid(row=2, column=2, padx=3, pady=2)
        self.Button_baseline3 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[2]))
        self.Button_baseline3.grid(row=2, column=3, padx=3, pady=2)
        self.Button_baseline3 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[2]))
        self.Button_baseline3.grid(row=2, column=4, padx=3, pady=2)


        # 4番目。i_numは3。
        if num_items == 3:
            return
        i_num = 3
        v = list_items[i_num]
        self.label_baseline4 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline4.grid(row=3, column=0, padx=3, pady=2)
        self.Button_baseline4 = tk.Button(self.Frame1, text='解析', command=lambda: self._calc_call(list_items[3]))
        self.Button_baseline4.grid(row=3, column=1, padx=3, pady=2)
        self.Button_baseline4 = tk.Button(self.Frame1, text='無視データ選択',
                                          command=lambda: self._ignore_call(list_items[3]))
        self.Button_baseline4.grid(row=3, column=2, padx=3, pady=2)
        self.Button_baseline4 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[3]))
        self.Button_baseline4.grid(row=3, column=3, padx=3, pady=2)
        self.Button_baseline4 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[3]))
        self.Button_baseline4.grid(row=3, column=4, padx=3, pady=2)

        # 5番目。i_numは4。
        if num_items == 4:
            return
        i_num = 4
        v = list_items[i_num]
        self.label_baseline5 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline5.grid(row=4, column=0, padx=3, pady=2)
        self.Button_baseline5 = tk.Button(self.Frame1, text='解析', command=lambda: self._calc_call(list_items[4]))
        self.Button_baseline5.grid(row=4, column=1, padx=3, pady=2)
        self.Button_baseline5 = tk.Button(self.Frame1, text='無視データ選択',
                                          command=lambda: self._ignore_call(list_items[4]))
        self.Button_baseline5.grid(row=4, column=2, padx=3, pady=2)
        self.Button_baseline5 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[4]))
        self.Button_baseline5.grid(row=4, column=3, padx=3, pady=2)
        self.Button_baseline5 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[4]))
        self.Button_baseline5.grid(row=4, column=4, padx=3, pady=2)
        if v['has_reference_data']:
            self.Button_baseline5 = tk.Button(self.Frame1, text='リファレンス選択',
                                              command=lambda: self._reference_call(list_items[4]))
            self.Button_baseline5.grid(row=4, column=5, padx=3, pady=2)


        # 6番目。i_numは5。
        if num_items == 5:
            return
        i_num = 5
        v = list_items[i_num]
        self.label_baseline6 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline6.grid(row=5, column=0, padx=3, pady=2)
        self.Button_baseline6 = tk.Button(self.Frame1, text='解析', command=lambda: self._calc_call(list_items[5]))
        self.Button_baseline6.grid(row=5, column=1, padx=3, pady=2)
        self.Button_baseline6 = tk.Button(self.Frame1, text='無視データ選択',
                                          command=lambda: self._ignore_call(list_items[5]))
        self.Button_baseline6.grid(row=5, column=2, padx=3, pady=2)
        self.Button_baseline6 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[5]))
        self.Button_baseline6.grid(row=5, column=3, padx=3, pady=2)
        self.Button_baseline6 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[5]))
        self.Button_baseline6.grid(row=5, column=4, padx=3, pady=2)

        # 7番目。i_numは6。
        if num_items == 6:
            return
        i_num = 6
        v = list_items[i_num]
        self.label_baseline7 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline7.grid(row=6, column=0, padx=3, pady=2)
        self.Button_baseline7 = tk.Button(self.Frame1, text='解析', command=lambda: self._calc_call(list_items[6]))
        self.Button_baseline7.grid(row=6, column=1, padx=3, pady=2)
        self.Button_baseline7 = tk.Button(self.Frame1, text='無視データ選択',
                                          command=lambda: self._ignore_call(list_items[6]))
        self.Button_baseline7.grid(row=6, column=2, padx=3, pady=2)
        self.Button_baseline7 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[6]))
        self.Button_baseline7.grid(row=6, column=3, padx=3, pady=2)
        self.Button_baseline7 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[6]))
        self.Button_baseline7.grid(row=6, column=4, padx=3, pady=2)

        # 8番目。i_numは7。
        if num_items == 7:
            return
        i_num = 7
        v = list_items[i_num]
        self.label_baseline8 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline8.grid(row=7, column=0, padx=3, pady=2)
        self.Button_baseline8 = tk.Button(self.Frame1, text='解析', command=lambda: self._calc_call(list_items[7]))
        self.Button_baseline8.grid(row=7, column=1, padx=3, pady=2)
        self.Button_baseline8 = tk.Button(self.Frame1, text='無視データ選択',
                                          command=lambda: self._ignore_call(list_items[7]))
        self.Button_baseline8.grid(row=7, column=2, padx=3, pady=2)
        self.Button_baseline8 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[7]))
        self.Button_baseline8.grid(row=7, column=3, padx=3, pady=2)
        self.Button_baseline8 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[7]))
        self.Button_baseline8.grid(row=7, column=4, padx=3, pady=2)

        # 9番目。i_numは8。
        if num_items == 8:
            return
        i_num = 8
        v = list_items[i_num]
        self.label_baseline9 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline9.grid(row=8, column=0, padx=3, pady=2)
        self.Button_baseline9 = tk.Button(self.Frame1, text='解析', command=lambda: self._calc_call(list_items[8]))
        self.Button_baseline9.grid(row=8, column=1, padx=3, pady=2)
        self.Button_baseline9 = tk.Button(self.Frame1, text='無視データ選択',
                                          command=lambda: self._ignore_call(list_items[8]))
        self.Button_baseline9.grid(row=8, column=2, padx=3, pady=2)
        self.Button_baseline9 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[8]))
        self.Button_baseline9.grid(row=8, column=3, padx=3, pady=2)
        self.Button_baseline9 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[8]))
        self.Button_baseline9.grid(row=8, column=4, padx=3, pady=2)

        # 10番目。i_numは9。
        if num_items == 9:
            return
        i_num = 9
        v = list_items[i_num]
        self.label_baseline10 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline10.grid(row=9, column=0, padx=3, pady=2)
        self.Button_baseline10 = tk.Button(self.Frame1, text='解析', command=lambda: self._calc_call(list_items[9]))
        self.Button_baseline10.grid(row=9, column=1, padx=3, pady=2)
        self.Button_baseline10 = tk.Button(self.Frame1, text='無視データ選択',
                                          command=lambda: self._ignore_call(list_items[9]))
        self.Button_baseline10.grid(row=9, column=2, padx=3, pady=2)
        self.Button_baseline10 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[9]))
        self.Button_baseline10.grid(row=9, column=3, padx=3, pady=2)
        self.Button_baseline10 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[9]))
        self.Button_baseline10.grid(row=9, column=4, padx=3, pady=2)

        # 11番目。i_numは10。
        if num_items == 10:
            return
        i_num = 10
        v = list_items[i_num]
        self.label_baseline11 = tk.Label(self.Frame1, text=v['item_display'])
        self.label_baseline11.grid(row=10, column=0, padx=3, pady=2)
        self.Button_baseline11 = tk.Button(self.Frame1, text='解析', command=lambda: self._calc_call(list_items[10]))
        self.Button_baseline11.grid(row=10, column=1, padx=3, pady=2)
        self.Button_baseline11 = tk.Button(self.Frame1, text='無視データ選択',
                                           command=lambda: self._ignore_call(list_items[10]))
        self.Button_baseline11.grid(row=10, column=2, padx=3, pady=2)
        self.Button_baseline11 = tk.Button(self.Frame1, text='トレンド表示',
                                          command=lambda: self._trend_open(list_items[10]))
        self.Button_baseline11.grid(row=10, column=3, padx=3, pady=2)
        self.Button_baseline11 = tk.Button(self.Frame1, text='データフォルダ',
                                          command=lambda: self._data_folder_open(list_items[10]))
        self.Button_baseline11.grid(row=10, column=4, padx=3, pady=2)

    def get_config_machine(self):
        self.config_ini = configparser.ConfigParser()
        list_machine = []
        for p in self.p_config.glob('setting*'):
            self.config_ini.read(p)
            list_machine.append(self.config_ini['DEFAULT']['machine_name'])
        return list_machine

    def _read_config(self, machine_name):
        v_list_machine = {}

        # 装置取得
        for p in self.p_config.glob('setting*'):
            self.config_ini = configparser.ConfigParser()
            self.config_ini.read(p, 'UTF-8')
            c_machine_name = self.config_ini['DEFAULT']['machine_name']
            if machine_name == c_machine_name:
                break
        else:
            raise SystemError('setting*.iniがありません')


        # 辞書取得
        list_items = []
        for i in self.config_ini.sections():
            v = {}
            for k, value in self.config_ini[i].items():
                if value == 'True':
                    v[k] = True
                elif value == 'False':
                    v[k] = False
                else:
                    v[k] = value
            list_items.append(v)
        return list_items

    # 解析ボタンを押されたとき
    def _calc_call(self, list_item):
        self.statusbar.configure(text='解析中...')
        self.statusbar.update()

        qc = QCAnalysis(list_item)
        qc.analysis()

        self.statusbar['text'] = f"{list_item['machine_name']} {list_item['item_display']}の解析完了"
        messagebox.showinfo('解析完了', f"{list_item['machine_name']} {list_item['item_display']}の解析完了")

    # ignoreリストを作成
    def _ignore_call(self, list_item):
        self.qc_i = QCAnalysis(list_item)
        self.list_all = self.qc_i.analysis(is_getdata=False)
        list_ignores = self.qc_i.read_ignore_list()
        list_ignore = [r[0] for r in list_ignores]
        # list_meas_tmpがない時は警告。
        if self.list_all is None:
            messagebox.showinfo('ファイルがありません。', '一度も解析していません。')
            return

        list_keyword = [r[0] for r in self.list_all]
        list_is_ignore = []
        for keyword in list_keyword:
            for ignore in list_ignore:
                if keyword == ignore:
                    list_is_ignore.append(True)
                    break
            else:
                list_is_ignore.append(False)

        num_list = len(list_keyword)

        self.sub_window = tk.Toplevel(self)
        self.sub_window.geometry('300x240')
        self.sub_window.title("無視をする結果の選択")
        self.sub_window.grab_set()
        self.sub_window.focus_set()
        self.sub_window.transient(self.master)

        self.canvas = tk.Canvas(self.sub_window, width=280, height=200)
        self.canvas.grid(row=1, rowspan=num_list, column=0, columnspan=5)
        self.scroll = ttk.Scrollbar(self.sub_window, orient=tk.VERTICAL)
        self.scroll.grid(row=1, rowspan=num_list, column=5, sticky='ns')

        self.scroll.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.scroll.set)
        self.sub_window.bind("<MouseWheel>", self.y_scrolling)

        # スクロール可動域＜＝これがないと、どこまでもスクロールされてしまう。
        sc_hgt = int(150 / 6 * (num_list + 1))  # スクロールの縦の範囲　リストの数＋ヘッダー分に
        self.canvas.config(scrollregion=(0, 0, 300, sc_hgt))

        self.sub_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.sub_frame,
                                  anchor=tk.NW, width=self.canvas.cget('width'))  # anchor<=NWで左上に寄せる

        irow = 2
        irow0 = 2
        erow = num_list + irow0

        self.list_chk = []
        while irow < erow:  # リストの数分ループしてLabelとチェックボックスを設置
            # チェックボックスの設置
            bln = tk.BooleanVar()

            # チェックボックスの初期値
            if list_is_ignore[irow - irow0]:
                bln.set(True)
            else:
                bln.set(False)
            c = tk.Checkbutton(self.sub_frame, variable=bln, width=2, text='')
            self.list_chk.append(bln)
            c.grid(row=irow, column=0, sticky=tk.NSEW)  # 0列目

            a1 = list_keyword[irow - irow0]
            b1 = tk.Label(self.sub_frame, width=20, text=a1)
            b1.grid(row=irow, column=1)  # 1列目

            irow = irow + 1

        # リストの下に設置するチェックボックスとボタン
        self.allSelectButton = tk.Button(self.sub_window, text='OK', command=self._subwindow_ok)
        self.allSelectButton.grid(row=erow, column=1)
        self.allClearButton = tk.Button(self.sub_window, text='Cancel', command=self._subwindow_ng)
        self.allClearButton.grid(row=erow, column=2)

    # リファレンス選択画面
    def _reference_call(self, list_item):
        self.qc_i = QCAnalysis(list_item)
        self.list_all = self.qc_i.analysis(is_getdata=False)
        list_refs = self.qc_i.read_ref_list()
        list_ref = [r[0] for r in list_refs]
        # list_meas_tmpがない時は警告。
        if self.list_all is None:
            messagebox.showinfo('ファイルがありません。', '一度も解析していません。')
            return

        list_keyword = [r[0] for r in self.list_all]
        list_is_ref = []
        for keyword in list_keyword:
            for ignore in list_ref:
                if keyword == ignore:
                    list_is_ref.append(True)
                    break
            else:
                list_is_ref.append(False)

        num_list = len(list_keyword)

        self.sub_window = tk.Toplevel(self)
        self.sub_window.geometry('300x240')
        self.sub_window.title("リファレンスとするデータの選択")
        self.sub_window.grab_set()
        self.sub_window.focus_set()
        self.sub_window.transient(self.master)

        self.canvas = tk.Canvas(self.sub_window, width=280, height=200)
        self.canvas.grid(row=1, rowspan=num_list, column=0, columnspan=5)
        self.scroll = ttk.Scrollbar(self.sub_window, orient=tk.VERTICAL)
        self.scroll.grid(row=1, rowspan=num_list, column=5, sticky='ns')

        self.scroll.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.scroll.set)
        self.sub_window.bind("<MouseWheel>", self.y_scrolling)

        # スクロール可動域＜＝これがないと、どこまでもスクロールされてしまう。
        sc_hgt = int(150 / 6 * (num_list + 1))  # スクロールの縦の範囲　リストの数＋ヘッダー分に
        self.canvas.config(scrollregion=(0, 0, 300, sc_hgt))

        self.sub_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.sub_frame,
                                  anchor=tk.NW, width=self.canvas.cget('width'))  # anchor<=NWで左上に寄せる

        irow = 2
        irow0 = 2
        erow = num_list + irow0

        self.list_chk = []
        while irow < erow:  # リストの数分ループしてLabelとチェックボックスを設置
            # チェックボックスの設置
            bln = tk.BooleanVar()

            # チェックボックスの初期値
            if list_is_ref[irow - irow0]:
                bln.set(True)
            else:
                bln.set(False)
            c = tk.Checkbutton(self.sub_frame, variable=bln, width=2, text='')
            self.list_chk.append(bln)
            c.grid(row=irow, column=0, sticky=tk.NSEW)  # 0列目

            a1 = list_keyword[irow - irow0]
            b1 = tk.Label(self.sub_frame, width=20, text=a1)
            b1.grid(row=irow, column=1)  # 1列目

            irow = irow + 1

        # リストの下に設置するチェックボックスとボタン
        self.allSelectButton = tk.Button(self.sub_window, text='OK', command=lambda: self._subwindow_ok(target='ref'))
        self.allSelectButton.grid(row=erow, column=1)
        self.allClearButton = tk.Button(self.sub_window, text='Cancel', command=self._subwindow_ng)
        self.allClearButton.grid(row=erow, column=2)

    # スクロールに関する部分。
    def y_scrolling(self, event):
        n = 10

        # 基本的にx_scrollingと同じですが、ybarはスクロールしたときのevent値がxbarと逆ですので注意！
        # マウスホイールをしたスクロールした場合：xbarはプラス、ybarはマイナス
        self.ybar_pos = self.scroll.get()
        self.ybar_wid = self.ybar_pos[1] - self.ybar_pos[0]
        self.move_yd = self.ybar_pos[0]

        self.ybar_max = 1 - self.ybar_wid

        # ybarの場合、マウスを上スクロールするとevent.deltaは負、下スクロールすると正の値を取得します。
        if event.delta < 0:
            self.n_splity = 1 * (self.ybar_max / n)
        elif event.delta > 0:
            self.n_splity = -1 * (self.ybar_max / n)
        else:
            self.n_spliyt = 1 * (self.ybar_max / n)

        self.move_yd += self.n_splity

        if self.move_yd < 0:
            self.move_yd = 0
        elif self.move_yd >= self.ybar_max:
            self.move_yd = self.ybar_max
        else:
            pass

        self.canvas.yview_moveto(self.move_yd)

    def _subwindow_ok(self, target='ignore'):
        # ignore listの場合
        if target == 'ignore':
            list_ignore = []
            for list_tmp, ignore_chk in zip(self.list_all, self.list_chk):
                if ignore_chk.get():
                    list_ignore.append(list_tmp)
            self.qc_i.write_ignore_list(list_ignore)

        # reference listの場合
        elif target == 'ref':
            list_ref = []
            for list_tmp, ref_chk in zip(self.list_all, self.list_chk):
                if ref_chk.get():
                    list_ref.append(list_tmp)
            self.qc_i.write_ref_list(list_ref)
        self.sub_window.destroy()


    def _subwindow_ng(self):
        self.sub_window.destroy()


    # トレンドを開く
    def _trend_open(self, list_item):
        p = list_item['trend_path'].replace('/', '\\')
        subprocess.Popen(["start", "", p], shell=True)


    def _data_folder_open(self, list_item):
        p = list_item['data_folder_path'].replace('/', '\\')
        subprocess.Popen(["explorer", p], shell=True)


if __name__ == '__main__':
    os.chdir('../')
    root = tk.Tk()
    QCApp(master=root)
    root.mainloop()



