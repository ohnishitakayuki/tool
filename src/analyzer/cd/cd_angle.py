import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path

import openpyxl

from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from getdf.convert_at import ConvertAt


class CdAngle:
    # Angle計算用
    angle_type = [0, 15, 30, 45, 60, 75, -90, -75, -60, -45, -30, -15]
    angle_scan = [270, 270, 45, 45, 45, 0, 0, 0, 315, 315, 315, 270]
    # 角度とスキャンタイプを分けている。補正で使用。
    angle_scan_type = {'p_angle': angle_type, 'scan_angle': angle_scan}
    ave_num = 25

    def __init__(self, p):
        df = self._convert_df(p)

        # 測定時間
        meas_start = df['meas_date'].min()
        meas_end = df['meas_date'].max()
        meas_time = meas_end - meas_start

        v_meas = {'meas_time': meas_time, 'meas_start': meas_start, 'meas_end': meas_end,}

        # 値
        v_value = self._calc_angle(df)

        # 結合してオブジェクト変数化
        v = v_meas | v_value
        for k in v:
            setattr(self, k, v[k])


    def _convert_df(self, p):
        # strかpathlibかわからんのでとりあえず変換。
        p = Path(p)
        if not p:
            raise FileNotFoundError('ファイルがありません。')
        if p.stat().st_size == 0:
            raise FileNotFoundError('ファイルが空です。')

        # 変換
        c = ConvertAt()
        df = c.df(p)

        if df.empty:
            raise FileNotFoundError('ファイルが空です。')

        return df

    def _calc_angle(self, df_org):
        # 深いコピーにして元df変更防止
        df = df_org.copy()
        df = self._get_angle(df)
        self.df_raw = df

        # 平均化
        df_ave = df.groupby('p_angle').agg({'cd1': 'mean', 'cd2': 'mean', 'cd3': 'mean',
                                            'cd4': 'mean', 'cd6': 'mean',}).reset_index()
        df_ave['ler'] = (df_ave['cd4'] + df_ave['cd6']) / 2

        # XY cd diff
        df_xy_ave = df_ave[(df_ave['p_angle'] == 0) | (df_ave['p_angle'] == -90)]
        xy_cd_diff = df_xy_ave['cd1'].max() - df_xy_ave['cd1'].min()
        xy_ler_diff = df_xy_ave['ler'].max() - df_xy_ave['ler'].min()

        # 45 cd diff
        df_45_ave = df_ave[(df_ave['p_angle'] == 0) | (df_ave['p_angle'] == 45) |
                            (df_ave['p_angle'] == -90) | (df_ave['p_angle'] == -45)]
        deg45_cd_diff = df_45_ave['cd1'].max() - df_45_ave['cd1'].min()
        deg45_ler_diff = df_45_ave['ler'].max() - df_45_ave['ler'].min()

        # Any angled
        angle_cd_diff = df_ave['cd1'].max() - df_ave['cd1'].min()
        angle_ler_diff = df_ave['ler'].max() - df_ave['ler'].min()

        # ler
        ler_hor = df_ave[df_ave['p_angle']==-90]['ler'].iloc[-1]
        ler_m45 = df_ave[df_ave['p_angle'] == -45]['ler'].iloc[-1]
        ler_ver = df_ave[df_ave['p_angle'] == 00]['ler'].iloc[-1]
        ler_p45 = df_ave[df_ave['p_angle'] == 45]['ler'].iloc[-1]

        # df
        self.df_ave = df_ave

        v = {'xy_cd_diff': xy_cd_diff, 'xy_ler_diff': xy_ler_diff, 'deg45_cd_diff': deg45_cd_diff,
             'deg45_ler_diff': deg45_ler_diff, 'angle_cd_diff': angle_cd_diff, 'angle_ler_diff': angle_ler_diff,
             'ler_hor': ler_hor, 'ler_m45': ler_m45, 'ler_ver':ler_ver, 'ler_p45': ler_p45}

        return v

    def _df_columns_cd_add(self, df, add_name):
        new_columns = []
        for column in df.columns:
            if 'cd' in column or 'AFQV' in column or 'PMQV' in column:
                new_columns.append(column + '_' + add_name)
            else:
                new_columns.append(column)
        df.columns = new_columns
        return df

    def _get_angle(self, df):
        df['p_angle'] = 0
        for i, a in enumerate(self.angle_type):
            df.loc[i * self.ave_num: (i+1) * self.ave_num, ['p_angle']] = a
        return df


if __name__ == '__main__':
    p = Path('../../test/test_data/data_cd_angle/MB3000_Angle_88nm_V01_P.000H.csv')
    c = CdAngle(p)
    print(vars(c))

