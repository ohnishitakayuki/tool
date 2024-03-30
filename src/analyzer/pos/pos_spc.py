import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from getdf.convert_lms import ConvertLms
from getdf.pos_correct import PosCorrect
from graph.net_graph import NetGraph


class PosSpc:
    def __init__(self, folder_baseline, search_baseline, sw=1):
        self.p_baseline = Path(folder_baseline)
        self.sw = sw

        df = self._df_average(self.p_baseline, search_baseline)
        df_baseline = df.groupby(['designX', 'designY']).agg({'X': 'mean', 'Y': 'mean'}).reset_index()
        df_baseline = df_baseline.rename(columns={'X': 'X_baseline', 'Y': 'Y_baseline'})
        self.df_baseline = df_baseline

    # ここから平均マップ作成
    def _df_average(self, p, search_word):
        # ファイル無いときはエラー
        if not (p):
            raise FileNotFoundError('ファイルがありません。')
        df = pd.DataFrame()
        for f in p.glob(f'{search_word}'):
            # print(f)
            if f.stat().st_size == 0:
                print('file is empty!!')
                continue
            try:
                df_tmp = self._convert(f)
            except ValueError:
                print('error')
                continue
            df = pd.concat([df, df_tmp])
        return df

    def _convert(self, f):
        c = ConvertLms(f)
        df = c.df(calc='simple')
        pos_cor = PosCorrect(df)
        df = pos_cor.correct_map(sw=self.sw)

        return df

    # 測定データ単体を指定
    def put_data(self, p_data):
        p = Path(p_data)
        if not (p):
            raise FileNotFoundError('ファイルがありません。')
        print(p)
        if p.stat().st_size == 0:
            raise FileNotFoundError('file is empty!!')
        try:
            df_data = self._convert(p)
        except ValueError:
            print('error')
        df = pd.merge(self.df_baseline, df_data, how='inner', on=['designX', 'designY'])
        df['X_diff'] = df['X'] - df['X_baseline']
        df['Y_diff'] = df['Y'] - df['Y_baseline']

        self.df_netgraph = df[['designX', 'designY', 'X_diff', 'Y_diff']]
        self.diff_3s_x = df['X_diff'].std() * 3
        self.diff_3s_y = df['Y_diff'].std() * 3
        self.meas_date = df['meas_date'].min()

    def netgraph(self, p, pitch_size=1, save_path='', name=''):
        self.put_data(p)
        g = NetGraph(self.df_netgraph)
        g.graph(pitch_size, self.meas_date, save_path)


if __name__ == '__main__':
    folder_baseline = '../../test/test_data/data_ipro8_spc/BaseLine/20230331_BaseLine/'
    path_data = '../../test/test_data/data_ipro8_spc/trend_data/20230912/2023091215x15_SPC_swath_Array_CTDconv.000.002.lms'
    search_baseline = '15x15_SPC_swath_Array*lms'
    c = PosSpc(folder_baseline, search_baseline=search_baseline, sw=1)
    c.put_data(path_data)
    print(c.diff_3s_x, c.diff_3s_y)



