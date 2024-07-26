import os
import sys
import pandas as pd
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from getdf.convert_prx import ConvertPrx
from pos_qc_lpos import PosQcLpos
from getdf.convert_lms import ConvertLms


class PosQcLpos2k(PosQcLpos):
    def __init__(self, p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2, calc='symmetry'):
        # 補正番号をリスト化
        self.sw = [0, 1, 2]
        self.calc = calc
        df1 = self._convert_df(p1)
        df2 = self._convert_df(p2)
        df_sl0_1 = self._convert_df(p_sl0_1)
        df_sl0_2 = self._convert_df(p_sl0_2)
        df_sl1_1 = self._convert_df(p_sl1_1)
        df_sl1_2 = self._convert_df(p_sl1_2)
        df_sl2_1 = self._convert_df(p_sl2_1)
        df_sl2_2 = self._convert_df(p_sl2_2)

        df_sl0 = self._average_sl(df_sl0_1, df_sl0_2)
        df_sl1 = self._average_sl(df_sl1_1, df_sl1_2)
        df_sl2 = self._average_sl(df_sl2_1, df_sl2_2)

        # csv化のためのコピー
        self.df1_org = df1.copy()
        self.df2_org = df2.copy()
        self.df_sl0_org = df_sl0.copy()
        self.df_sl1_org = df_sl1.copy()
        self.df_sl2_org = df_sl2.copy()

        # 測定時間
        meas_start_1st = df1['meas_date'].min()
        meas_end_1st = df1['meas_date'].max()
        meas_start_2nd = df2['meas_date'].min()
        meas_end_2nd = df2['meas_date'].max()
        meas_time_1st = meas_end_1st - meas_start_1st
        meas_time_2nd = meas_end_2nd - meas_start_2nd
        v_meas = {'meas_time_1st': meas_time_1st, 'meas_start_1st': meas_start_1st, 'meas_end_1st': meas_end_1st,
                  'meas_time_2nd': meas_time_2nd, 'meas_start_2nd': meas_start_2nd, 'meas_end_2nd': meas_end_2nd}

        # Field座標などを追加
        df1 = self._arrange_data(df1)
        df2 = self._arrange_data(df2)

        # SLは別関数。2つ送って平均化。
        df1_sl = self._arrange_sl(df_sl0, df_sl1)
        df2_sl = self._arrange_sl(df_sl1, df_sl2)

        # SL補正
        df1 = pd.merge(df1, df1_sl[['X_sl', 'Y_sl', 'fieldX', 'fieldY']], how='left', on=['fieldX', 'fieldY'])
        df2 = pd.merge(df2, df2_sl[['X_sl', 'Y_sl', 'fieldX', 'fieldY']], how='left', on=['fieldX', 'fieldY'])

        df1['X'] = df1['X'] - df1['X_sl']
        df1['Y'] = df1['Y'] - df1['Y_sl']
        df2['X'] = df2['X'] - df2['X_sl']
        df2['Y'] = df2['Y'] - df2['Y_sl']

        df1['designX'] = df1['designX'] + df1['fieldX']
        df1['designY'] = df1['designY'] + df1['fieldY']
        df2['designX'] = df2['designX'] + df2['fieldX']
        df2['designY'] = df2['designY'] + df2['fieldY']

        # 補正
        v_tmp = self._calc_rep(df1, df2)
        v_coef1 = self._calc_coef(df1, 'data1')
        v_coef2 = self._calc_coef(df2, 'data2')

        # 辞書結合
        v = v_meas | v_tmp | v_coef1 | v_coef2

        for k in v:
            setattr(self, k, v[k])

    # symmetryとThresholdの切り替えのため、オーバーライド
    def _convert_df(self, p):
        # クラス変数をローカルに持ってくる。
        calc = self.calc
        # strかpathlibかわからんのでとりあえず変換。
        p = Path(p)
        if not(p.exists()):
            raise FileNotFoundError('ファイルがありません。')
        if p.stat().st_size == 0:
            raise FileNotFoundError('ファイルが空です。')

        # 変換。拡張子でファイルタイプ確認。
        if p.suffix == '.lms':
            c = ConvertLms(p)
            df = c.df(calc='lpos')
        elif p.suffix == '.prx':
            if calc == 'symmetry':
                c = ConvertPrx(p)
                df = c.df(calc='lpos')
            elif calc == 'lpos_threshold':
                c = ConvertPrx(p)
                df = c.df(calc='lpos_threshold')
            else:
                raise FileNotFoundError('calcが正しくありません。')
        else:
            raise FileNotFoundError('ファイルが対応している拡張子ではありません。')

        return df

    def _average_sl(self, df1, df2):
        df2 = df2[['fieldX', 'fieldY', 'X', 'Y']]
        df2 = df2.rename(columns={'X':'X_2nd', 'Y': 'Y_2nd'})
        df = pd.merge(df1, df2, how='inner', on=['fieldX', 'fieldY'])
        df['X'] = (df['X'] + df['X_2nd']) / 2
        df['Y'] = (df['Y'] + df['Y_2nd']) / 2
        df = df.drop('X_2nd', axis=1)
        df = df.drop('Y_2nd', axis=1)
        return df

    def _arrange_data(self, df):
        # PROVEは特にデータをいじくる必要はない。
        return df

    def _arrange_sl(self, df1, df2):
        df2 = df2.rename(columns={'X': 'X_2nd', 'Y': 'Y_2nd'})
        df = pd.merge(df1, df2[['fieldX', 'fieldY', 'X_2nd', 'Y_2nd']], how='inner', on=['fieldX', 'fieldY'])
        df['X'] = (df['X'] + df['X_2nd']) / 2
        df['Y'] = (df['Y'] + df['Y_2nd']) / 2
        df = df.drop(['X_2nd', 'Y_2nd'], axis=1)
        df['num'] = range(1, len(df.index) + 1)
        f_num = self.field_num
        f_size = self.field_size
        df['X'] = df['X'] - df['fieldX']
        df['Y'] = df['Y'] - df['fieldY']
        df = df.rename(columns={'X':'X_sl', 'Y':'Y_sl'})
        df = df.drop('num', axis=1)
        return df


if __name__ == '__main__':
    p1 = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_16-51-10.prx')
    p2 = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_17-03-53.prx')
    p_sl0_1 = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-44-25.prx')
    p_sl0_2 = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_16-48-01.prx')
    p_sl1_1 = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-57-14.prx')
    p_sl1_2 = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-00-48.prx')
    p_sl2_1 = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_17-10-01.prx')
    p_sl2_2 = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-13-33.prx')
    c = PosQcLpos2k(p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2, calc='lpos_threshold')
    # c = PosQcLpos2k(p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2)
    print(vars(c))