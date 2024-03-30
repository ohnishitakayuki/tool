import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path
from pos.pos_spc import PosSpc


class PosSpcCalc:
    def __init__(self, path_baseline, path_data, search_baseline, search_word, sw, max_meas):
        self.p_baseline = Path(path_baseline)
        self.p_data = Path(path_data)
        self.search_baseline = search_baseline
        self.search_word = search_word
        self.sw = sw
        self.max_meas = max_meas

        # ファイルのリストを取得。maxまでの数に制限している。
        list_f = self._get_list_f()

        # データフレーム形式で取得
        self.df_all = self._get_df(list_f).reset_index().drop('index', axis=1)
        df_ave = self.df_all.groupby('date_num').agg({'meas_date': 'min', '3s_x': 'max', '3s_y': 'max'}).reset_index()
        self.df_ave = df_ave.sort_values('meas_date')

    def _get_list_f(self):
        # パスリストを取得。測定最後の3つを取得するように計算
        c = PosSpc(self.p_baseline, self.search_baseline, self.sw)
        list_f = []
        p_data_sorted = sorted(self.p_data.glob('*'))
        for p_data_date in p_data_sorted:
            list_f_date = []
            for f in p_data_date.glob(self.search_word):
                meas_time = os.path.getmtime(f)
                list_f_date_tmp = [meas_time, f]
                list_f_date.append(list_f_date_tmp)
            list_f_date = sorted(list_f_date)
            if self.max_meas != 0:
                list_f_date = list_f_date[-self.max_meas:]
            list_f.append(list_f_date)
        return list_f

    def _get_df(self, list_f):
        c = PosSpc(self.p_baseline, search_baseline=self.search_baseline, sw=self.sw)
        df = pd.DataFrame()
        for i, list_f_date in enumerate(list_f):
            for j, list_d in enumerate(list_f_date):
                try:
                    c.put_data(list_d[1])
                except ValueError:
                    print('Value Error発生')
                    continue
                df_tmp = pd.DataFrame({'meas_date': [c.meas_date],
                                       'date_num': [i+1],
                                       'meas_num': [j+1],
                                       '3s_x': [c.diff_3s_x],
                                       '3s_y': [c.diff_3s_y],
                })
                df = pd.concat([df, df_tmp])
        df = df.sort_values('meas_date')
        return df

    def graph(self, p_save=''):
        df = self.df_ave

        fig, ax = plt.subplots()
        ax.plot(df['meas_date'], df['3s_x'], marker='o', label='X')
        ax.plot(df['meas_date'], df['3s_y'], marker='o', label='Y')
        ax.set_title(f'SPC Trend')
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        ax.set_ylabel('3S from a baseline[nm]')
        ax.set_yticks(np.arange(0, 2, 0.2))
        ax.set_ylim(0, 1)
        if not (p_save):
            return fig, ax
        else:
            plt.savefig(p_save)

    def netgraph(self, p_save, pitch_size):
        list_f = self._get_list_f()
        c = PosSpc(self.p_baseline, search_baseline=self.search_baseline, sw=self.sw)
        df = pd.DataFrame()
        for i, list_f_date in enumerate(list_f):
            for j, list_d in enumerate(list_f_date):
                try:
                    date_str = datetime.fromtimestamp(list_d[0]).strftime('%Y/%m/%d %H:%M:%S')
                    date_str_save = datetime.fromtimestamp(list_d[0]).strftime('%Y%m%d_%H%M%S')
                    save_str = f'{p_save}/{date_str_save}'
                    c.netgraph(list_d[1], pitch_size=pitch_size, save_path=save_str, name=date_str)
                except ValueError:
                    print('Value Error発生')
                    continue


if __name__ == '__main__':
    path_baseline = '../test/test_data/data_ipro8_spc/BaseLine/20230331_BaseLine/'
    path_data = '../test/test_data/data_ipro8_spc/trend_data/'
    search_baseline = '15x15_SPC_swath_Array*lms'
    search_word = '*15x15_SPC_swath_Array*lms'
    t = PosSpcCalc(path_baseline, path_data, search_baseline, search_word, sw=1, max_meas=3)
    print(t.df_ave)
