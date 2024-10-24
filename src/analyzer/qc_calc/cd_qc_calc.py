import os
import sys
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime
import openpyxl
import dateutil
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from file.file_collector import FileCollector


class CdQcCalc:
    p_mid = ''
    ignore_list_name = ''
    reference_list_name = 'dummy'
    list_meas_tmp = 'list_meas_tmp.pkl'
    search_meas_file = 'xxxxxxxxx'

    # ignore listの読み込み
    def __init__(self, p, p_mid, p_from, is_reload=False, search_plate=False, search_word=False):
        self.p = p
        self.p_from = p_from
        self.list_meas_set = []
        self.is_reload = is_reload
        self.search_plate = search_plate
        if search_word:
            self.search_word = search_word
            self.search_meas_file = f'**/{search_word}'


        # 中間ファイルの処理。Noneの時はpフォルダにmid_dataフォルダを勝手に作る。
        if p_mid is None:
            self.p_mid = Path(p / 'mid_data')
        else:
            self.p_mid = p_mid
        if not(self.p_mid.exists()):
            self.p_mid.mkdir(parents=True)

        self.p_ignore = Path(str(self.p_mid) + '/' + self.ignore_list_name)
        self.p_ref = Path(str(self.p_mid) + '/' + self.reference_list_name)

        # ignoreリストの読み込み。ない時はスキップ
        if self.p_ignore.exists():
            with open(self.p_ignore, 'rb') as f:
                self.list_ignore = pickle.load(f)
        else:
            self.list_ignore = []

        # referenceリストの読み込み。解析的に必要なものに適用。ない時はスキップ。
        if self.p_ref.exists():
            with open(self.p_ref, 'rb') as f:
                self.list_ref = pickle.load(f)
        else:
            self.list_ref = []

        # 解析リスト(list_meas)の一時ファイルのpathlib化。appのignore読み込み高速化で使用。
        self.p_list_meas_tmp = Path(str(self.p_mid) + '/' + self.list_meas_tmp)

        # ファイルコピー、p_fromがない時はスキップ
        if p_from:
            f = FileCollector(self.p_from, self.p, is_newfile=False, is_filesize_check=True)
            f.collect(search_word=self.search_word)

        # 測定リストを作成する
        self.get_result_list()

    def get_result_list(self):
        list_meas_row = []

        # 作成時刻とパスでリストを作ってから、作成時刻順でソート
        for f in self.p.glob(self.search_meas_file):
            # ファイルが空の時はリストに入れない。
            if f.stat().st_size == 0:
                continue
            meas_time = datetime.fromtimestamp(f.stat().st_mtime)
            # search_plateがonのとき、ファイルが入っているフォルダの名前を取得。

            if self.search_plate:
                plate_name = f.parents[1].name
            else:
                plate_name = ''
            list_tmp = [meas_time, str(f), plate_name]
            list_meas_row.append(list_tmp)
        list_meas_row = sorted(list_meas_row)
        list_meas = self._get_meas_combination(list_meas_row)
        self.list_meas = list_meas

        # list_measを一時ファイルとしてpickle化。Appのignoreリストで使用。
        with open(self.p_list_meas_tmp, 'wb') as f:
            pickle.dump(list_meas, f)


    def _get_meas_combination(self, list_meas_row):
        # 組み合わせを探す必要ないときはこれでOK。
        list_meas = list_meas_row
        return list_meas

    def write_ignore_list(self, list_ignore):
        """
        ignore_listの書き込み。ファイルとインスタンス変数に書き込んでいる
        """
        with open(self.p_ignore, 'wb') as f:
            pickle.dump(list_ignore, f)
        self.list_ignore = list_ignore

    def write_ref_list(self, list_ref):
        """
        ref_listの書き込み。ファイルとインスタンス変数に書き込んでいる
        """
        with open(self.p_ref, 'wb') as f:
            pickle.dump(list_ref, f)
        self.list_ref = list_ref

    def _get_list_real_meas(self, list_meas, list_ignore):
        """
        list_measの中にあるlist_ignoreに入っているものを削除する関数
        """
        list_real_meas = []
        for list_meas_tmp in list_meas:
            for list_ignore_tmp in list_ignore:
                if list_meas_tmp == list_ignore_tmp:
                    break
            else:
                list_real_meas.append(list_meas_tmp)
        return list_real_meas

    # トレンド生成
    def _collect_result(self):
        list_meas = self._adapt_ref(self.list_meas)
        list_real_meas = self._get_list_real_meas(list_meas, self.list_ignore)
        list_result = []
        for list_meas_set in list_real_meas:
            try:
                r = self._get_pickle(list_meas_set)
            except TypeError:
                print('Type Error発生')
                continue
            except dateutil.parser._parser.ParserError:
                print('parser Error発生')
                continue
            except pd._libs.tslibs.parsing.DateParseError:
                print('parser Error pandas起因発生')
                continue
            except ValueError:
                print('Value Error発生')
                continue
            except FileNotFoundError:
                print('ファイルが空なのでError')
                continue
            except AttributeError:
                print('解析がうまくいかなかったのでError')
                continue
            except KeyError:
                print('シート内にカラムが無かったのでError')
                continue

            # ある値が超えた場合にスキップする関数。関数そのものは継承先で記述。
            if self._qc_check_value(r):
                list_result.append(r)
        return list_result

    # refを適用する関数。継承で使用。refを使用しない物に対してはそのままスルーする。
    def _adapt_ref(self, list_meas):
        return list_meas

    def _get_pickle(self, list_meas_set):
        """
        オブジェクトがない場合は生成。ある場合は読み込み。
        生成時は保存も行う。
        また、is_reloadがTrueの時はファイルの有無にかかわらず再読み込み。
        """
        meas_time = list_meas_set[0]
        f_name = f"{meas_time.strftime('%Y%m%d_%H%M%S_%f')}.pkl"
        p = Path(f'{str(self.p_mid)}/{f_name}')
        if not(self.is_reload) and p.exists():
            print('Pickle file is read.', p)
            with open(p, 'rb') as f:
                c = pickle.load(f)
        else:
            c = self._read_pickle(list_meas_set)
            print('Pickle file is created.', p)
            with open(p, 'wb') as f:
                pickle.dump(c, f)

        return c

    def _read_pickle(self, **kwargs):
        # pickleファイルを読み込むダミー。継承先で作ってね。
        return None

    def save_result_csv(self, p=False):
        # 各継承先で作成するので、ここはダミー
        raise SystemError('継承してから使用してください。')

    # Excelファイル作成
    def save_excels(self, p_save):
        list_instance = self._collect_result()
        if not(p_save.exists()):
            p_save.mkdir(parents=True)
        for r in list_instance:
            meas_time = self._get_meas_time(r)
            excel_file_name = f'{self.excel_file_stem}_{meas_time}.xlsx'
            p = Path(p_save / excel_file_name)
            if not(p.exists()):
                try:
                    r.to_excel(p)
                except KeyError:
                    print('Making Excel File is fault.')
                print('Excel file is created.', p)
            else:
                print('Excel file is existed.', p)

    def _get_meas_time(self, r):
        # 測定によって測定時間の名前が違うため、関数で取得。基本は"meas_start"
        meas_time = r.meas_start.strftime('%Y%m%d_%H%M%S')
        return meas_time

    # Excel Trendファイル作成
    def save_excel_trend(self, p_trend):
        # Excelのトレンドシートにデータを貼り付ける
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            # tryでエラーははじこう
            try:
                list_result_tmp = self._get_list_result_tmp(r)
            except AttributeError:
                print('空データのため、Attribute Error発生。')
                continue

            list_result.append(list_result_tmp)
        df = pd.DataFrame(list_result)
        wb = openpyxl.load_workbook(self.p_trend_format)
        ws = wb['Trend']
        self._write_excel(df, ws)
        wb.save(p_trend)

    def _write_excel(self, df, ws, offset_columns=0):
        for j in range(len(df)):
            for i in range(len(df.columns)):
                ws.cell(row=self.excel_start_row+j, column=self.excel_start_column+offset_columns+i,
                        value=df.iloc[j, i])

    def _get_list_result_tmp(self, r):
        # Excel Trendリストを作成する関数。継承先で作成
        raise SystemError('継承してから使用してください。')

    def _qc_check_value(self, r):
        # 継承先で記述する、データをはじくための文章。継承元では必ずTrueにする。
        return True