import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import timedelta
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from getdf.convert_lms import ConvertLms
from getdf.pos_correct import PosCorrect
from analyzer.pos.pos_stability import PosStability


class PosStabilityCalc:
    same_load_time = 20  # 同一測定かを見破る時間設定。この時間を超えた場合は別ロードとして認定。単位:分

    def __init__(self, p_data, same_load=False, average_num=10, sw=1): # sw=1なのでRotation補正
        self.p_data = Path(p_data)
        self.same_load = same_load
        self.average_num = average_num
        self.sw = sw
        self.df_stab = None
        self.calc()

    def calc(self):
        # 本来は疎結合にして、変換も関数先で行いたいが、移動平均があるため、変換が多くなる。
        # 先に変換、dfリスト化してからforループ。
        list_df = self._get_list_df()
        # same_loadで切り分け
        if self.same_load:
            df = self._get_same_load_df(list_df)
        else:
            df = self._get_moving_df(list_df)

        # クラス変数にしとく
        self.df_stab = df

    def graph(self, p_save=''):
        df = self.df_stab
        fig, ax = plt.subplots()
        ax.plot(df['meas_date'], df['x'], marker='o', label='x')
        ax.plot(df['meas_date'], df['y'], marker='o', label='y')
        ax.set_title(f'Position Stability')
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.set_ylabel('Repeatability 3s [nm]')
        ax.set_yticks(np.arange(0, 2, 0.2))
        ax.set_ylim(0, 1)
        plt.legend()
        if not(p_save):
            return fig, ax
        else:
            plt.savefig(p_save)

    def _get_same_load_df(self, list_df):
        # 同じロード内で求める場合
        spec_time = timedelta(minutes=self.same_load_time)
        list_x = []
        list_y = []
        list_meas_date = []
        list_df_tmp = []
        list_num = []
        end_time = False
        for df in list_df:
            if not end_time:
                # 初回は判定をスルーする。
                list_df_tmp.append(df)
                end_time = df['meas_date'].iloc[-1]
                continue
            start_time = df['meas_date'].iloc[0]
            blank_time = start_time - end_time
            if blank_time < spec_time:
                # 連続測定のとき、list_df_tmpにdfを追加してコンティニュー
                list_df_tmp.append(df)
                end_time = df['meas_date'].iloc[-1]
                continue

            # 以下アンロード/ロードがあった場合の処理
            # 計算
            list_df_tmp.append(df)
            if len(list_df_tmp) > 1:  # 1個しかデータがない場合はスキップ
                c = PosStability(list_df_tmp)
                stab_x, stab_y = c.stab()
                meas_date = c.meas_date()
                list_x.append(stab_x)
                list_y.append(stab_y)
                list_meas_date.append(meas_date)
                list_num.append(len(list_df_tmp))

            # 終了処理
            end_time = False
            list_df_tmp = []
        else:     # forループ最後にもう一度計算
            if len(list_df_tmp) > 1:  # 1個しかデータがない場合はスキップ
                c = PosStability(list_df_tmp)
                stab_x, stab_y = c.stab()
                meas_date = c.meas_date()
                list_x.append(stab_x)
                list_y.append(stab_y)
                list_meas_date.append(meas_date)
                list_num.append(len(list_df_tmp))

        df = pd.DataFrame({'meas_date': list_meas_date,
                           'x': list_x,
                           'y': list_y,
                           'data_num': list_num})
        return df

    def _get_moving_df(self, list_df):
        # 移動平均で求める場合
        list_x = []
        list_y = []
        list_meas_date = []
        list_num = []
        for i in range(len(list_df)-self.average_num):
            list_df_calc = list_df[i: i+self.average_num]
            c = PosStability(list_df_calc)
            stab_x, stab_y = c.stab()

            meas_date = c.meas_date()
            list_x.append(stab_x)
            list_y.append(stab_y)
            list_meas_date.append(meas_date)
            list_num.append(len(list_df_calc))
        df = pd.DataFrame({'meas_date':list_meas_date,
                           'x': list_x,
                           'y': list_y,
                           'data_num': list_num})
        return df

    def _get_list_df(self):
        # dfをまとめたリストを作成する。
        list_df = []
        p = list(Path(self.p_data).glob('*.lms'))

        if not(p):
            raise FileNotFoundError('ファイルがありません。')
        p.sort(key=os.path.getmtime)
        for f in p:
            print(f)
            if f.stat().st_size == 0:
                print('file is empty!!')
                continue
            try:
                df = self._convert(f)
            except ValueError:
                print('error')
                continue
            list_df.append(df)
        return list_df

    def _convert(self, f):
        c = ConvertLms(f)
        df = c.df(calc='simple')
        pos_cor = PosCorrect(df)
        df = pos_cor.correct_map(sw=self.sw)

        return df


if __name__ == '__main__':
    t = PosStabilityCalc('../test/test_data/data_pos_stability_calc/', same_load=False, average_num=20, sw=2)
    print(t.df_stab)