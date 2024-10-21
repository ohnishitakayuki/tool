import numpy as np
import pandas as pd

from pathlib import Path
import pathlib

class ConvertEmu:
    def __init__(self):
        pass

    def df(self, p):
        # strとpatlib両方対応
        if not type(p) is pathlib.WindowsPath:
            p = Path(p)

        # 読み込みと整形
        df_tmp = pd.read_csv(p)
        df_tmp['meas_date'] = pd.to_datetime(df_tmp['Date'])
        df = df_tmp[['meas_date']]
        df = pd.concat([df, df_tmp[['SamplePosX', 'SamplePosY',
                    'Layer1 Col', 'Layer1 Row', 'Beam Rotation']]], axis=1)
        df = df.rename(columns={'SamplePosX': 'design_pos_x', 'SamplePosY': 'design_pos_y',
                     'Layer1 Col': 'die_x', 'Layer1 Row': 'die_y', 'Beam Rotation': 'rotation'})

        # 複数カラムがあるときの変換。
        list_columns = df_tmp.columns
        list_columns = list(filter(lambda x: x.startswith('ViewMeasPoint'), list_columns))
        list_columns = [s for s in list_columns if 'Angle' not in s]

        for i, columns in enumerate(list_columns):
            idx = i + 1
            df_tmp2 = df_tmp[[f'ViewMeasPoint{idx}', f'L-3Sig{idx}', f'R-3Sig{idx}']]
            df_tmp2 = df_tmp2.rename(
                columns={f'ViewMeasPoint{idx}': f'cd{idx}',
                         f'L-3Sig{idx}': f'LER_left{idx}', f'R-3Sig{idx}': f'LER_right{idx}', })
            df_tmp2[f'cd{idx}'] = df_tmp2[f'cd{idx}'].astype(float)
            df = pd.concat([df, df_tmp2], axis=1)
        df = df.replace('--', np.nan)

        return df


if __name__ == '__main__':
    p = Path('../../../data/ResultMain.CSV')
    t = ConvertEmu()
    df = t.df(p)
    print(df)