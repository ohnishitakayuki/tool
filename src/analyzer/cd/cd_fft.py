import numpy as np
import pandas as pd
from scipy import signal


class CDFft:
    def __init__(self, f):
        df_l, df_r = self._get_df(f)

        # dfをマージ
        df_l = df_l.rename(columns={'edge': 'edge_left'})
        df_r = df_r.rename(columns={'edge': 'edge_right'})
        df = pd.merge(df_l, df_r, how='inner', on='pos')
        df['lwr'] = df['edge_right'] - df['edge_left']
        self.df = df

    def df_fft(self, pixel, edge_type):
        df_a = self.df.copy()
        # ピクセル処理
        if pixel is None:
            pixel = len(df_a)
        start_pixel = int((len(df_a) - pixel) / 2)
        end_pixel = int(len(df_a) - (len(df_a) - pixel) / 2)
        df = df_a.iloc[start_pixel: end_pixel]

        # FFT処理
        freq, pow = self._fft_edge(df, edge_type)
        df_fft = pd.DataFrame(data={'freq': freq, 'pow': pow})
        return df_fft

    def _get_df(self, f):
        df = pd.read_csv(f)

        # 1つめのFieldしか有効にしない処理
        first_field = df.loc[0, 'Field']
        df = df[df['Field'] == first_field]

        # left edgeとright edgeの抜き出し
        df_l = df[['Y1', 'X1']]
        df_r = df[['Y2', 'X2']]

        # XかYの判定
        direction = df.loc[0, 'Label'][-1]
        if direction == 'X':
            df_l = df_l.rename(columns={'Y1': 'pos', 'X1': 'edge'})
            df_r = df_r.rename(columns={'Y2': 'pos', 'X2': 'edge'})
        elif direction == 'Y':
            df_l = df_l.rename(columns={'Y1': 'edge', 'X1': 'pos'})
            df_r = df_r.rename(columns={'Y2': 'edge', 'X2': 'pos'})
        else:
            raise ValueError('解析できないスキャン方向の可能性があります。')

        # 並び替え
        df_l = df_l[['pos', 'edge']]
        df_r = df_r[['pos', 'edge']]

        return df_l, df_r

    # FFT解析用
    def _fft_edge(self, df, edge_type):
        df = df.reset_index()
        f = df[edge_type].values
        dl = abs(df['pos'][1] - df['pos'][0])
        N = len(df['pos'])
        freq = np.linspace(0, 1 / dl, N)
        f = f - f.mean()
        f = signal.detrend(f)
        self.df_fft_row = pd.DataFrame(f)
        F = np.fft.fft(f)
        Amp = np.abs(F) / N
        Pow = Amp ** 2
        return freq, Pow


if __name__ == '__main__':
    t = CDFft('../../test/test_data/data_cd_fft/27_ASI_160pA_GLCD_88_256pt_v1_510H_L6.000.A00005005S0001_00.csv')
    df = t.df_fft(512, 'edge_left')
    # df.to_csv('../../t2.csv')
    print(df)
    print(df['pow'].sum())
