import os
import sys
import pandas as pd
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from getdf.convert_prx import ConvertPrx


class PosLocalPos:
    def __init__(self, p, p_sl1, p_sl2, p_sl3, p_sl4):
        df = self._convert_df(p)
        df_sl1 = self._convert_df(p_sl1)
        df_sl2 = self._convert_df(p_sl2)
        df_sl3 = self._convert_df(p_sl3)
        df_sl4 = self._convert_df(p_sl4)

        # 解析
        v = self._calc(df, df_sl1, df_sl2, df_sl3, df_sl4)

    def _convert_df(self, p):
        # strかpathlibかわからんのでとりあえず変換。
        p = Path(p)

        if not(p.exists()):
            raise FileNotFoundError('ファイルがありません。')
        if p.stat().st_size == 0:
            raise FileNotFoundError('ファイルが空です。')

        # 変換。拡張子でファイルタイプ確認。
        if p.suffix == '.prx':
            c = ConvertPrx(p)
        else:
            raise FileNotFoundError('ファイルが対応している拡張子ではありません。')

        df = c.df()
        return df

    def _calc(self, df_org, df_sl1_org, df_sl2_org, df_sl3_org, df_sl4_org):
        # 深いコピーにして元df変更防止
        df = df_org.copy()
        df.to_csv('../../../t4.csv')
        df_sl1 = df_sl1_org.copy()
        df_sl2 = df_sl2_org.copy()
        df_sl3 = df_sl3_org.copy()
        df_sl4 = df_sl4_org.copy()

        # sl番号追加
        df_sl1['SL'] = 1
        df_sl2['SL'] = 2
        df_sl3['SL'] = 3
        df_sl4['SL'] = 4

        # マージと平均
        df_sl = pd.concat([df_sl1, df_sl2])
        df_sl = pd.concat([df_sl, df_sl3])
        df_sl = pd.concat([df_sl, df_sl4])
        df_sl = df_sl[['X', 'Y', 'X_roi', 'Y_roi']]

        df_sl_ave = df_sl.groupby(['X_roi', 'Y_roi']).mean().reset_index()
        df_sl_ave['X'] = df_sl_ave['X'] - df_sl_ave['X'].mean()
        df_sl_ave['Y'] = df_sl_ave['Y'] - df_sl_ave['Y'].mean()
        df_sl_ave = df_sl_ave.rename(columns={'X': 'X_sl', 'Y': 'Y_sl'})

        df = pd.merge(df, df_sl_ave, how='inner', on=['X_roi', 'Y_roi'])
        print(df_sl_ave)
        df['X'] = df['X'] - df['X_sl']
        df['Y'] = df['Y'] - df['Y_sl']

        print(df)
        df.to_csv('../../../t3.csv')





if __name__ == '__main__':
    p = Path('../../test/test_data/data_pos_local_pos/LPOS35X35_ARRAY3X3_N5_MB_B_2023-12-12_1_12-55-24.prx')
    p_sl1 = Path('../../test/test_data/data_pos_local_pos/LPOS35X35JINBEISL_2023-12-12_1_12-47-26.prx')
    p_sl2 = Path('../../test/test_data/data_pos_local_pos/LPOS35X35JINBEISL_2023-12-12_1_13-55-52.prx')
    p_sl3 = Path('../../test/test_data/data_pos_local_pos/LPOS35X35JINBEISL_2023-12-12_2_12-51-37.prx')
    p_sl4 = Path('../../test/test_data/data_pos_local_pos/LPOS35X35JINBEISL_2023-12-12_2_14-00-06.prx')
    c = PosLocalPos(p, p_sl1, p_sl2, p_sl3, p_sl4)