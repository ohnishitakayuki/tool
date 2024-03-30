import numpy as np
import pandas as pd

from pathlib import Path
import pathlib

class ConvertAt:
    def __init__(self):
        pass

    def df(self, p, is_cd_collect=False):
        # strとpatlib両方対応
        if not type(p) is pathlib.WindowsPath:
            p = Path(p)

        # 読み込みと整形
        df_tmp = pd.read_csv(p)
        df_tmp = df_tmp.replace({999: np.nan, '': np.nan, '--': np.nan})
        df_tmp['meas_date'] = pd.to_datetime(df_tmp['<DATE>'] + ' ' + df_tmp['<TIME>'])
        df = df_tmp[['meas_date']]
        df = pd.concat([df, df_tmp[['<XDPS>', '<YDPS>', '<XPOS>', '<YPOS>', '<ZPOS>',
                    '<COLA>', '<ROWA>', '<SITE>', '<ROTA>', '<AFQV>', '<PMQV>', '<SCAN>']]], axis=1)
        df = df.rename(columns={'<XDPS>': 'design_pos_x',
                    '<YDPS>': 'design_pos_y', '<XPOS>': 'real_pos_x', '<YPOS>': 'real_pos_y',
                     '<ZPOS>': 'real_pos_z', '<COLA>': 'die_x', '<ROWA>': 'die_y', '<SITE>': 'site',
                     '<ROTA>': 'rotation', '<AFQV>': 'AFQV', '<PMQV>': 'PMQV', '<SCAN>': 'scan'})

        # 複数カラムがあるときの変換。
        list_columns = df_tmp.columns
        list_columns = list(filter(lambda x: x.startswith('<CD'), list_columns))
        if is_cd_collect:
            cd_text = 'CCD'
        else:
            cd_text = 'CD_'
        for i, columns in enumerate(list_columns):
            idx = i + 1
            df_tmp2 = df_tmp[[f'<XFDP{idx}>', f'<YFDP{idx}>', f'<LBL{idx}>', f'<{cd_text}{idx}>', f'<DES{idx}>']]
            df_tmp2 = df_tmp2.rename(
                columns={f'<XFDP{idx}>': f'design_pos_x_ROI{idx}', f'<YFDP{idx}>': f'design_pos_y_ROI{idx}', \
                         f'<LBL{idx}>': f'label{idx}', f'<{cd_text}{idx}>': f'cd{idx}',
                         f'<DES{idx}>': f'design_size{idx}'})
            df_tmp2[f'cd{idx}'] = df_tmp2[f'cd{idx}'].astype(float)
            df_tmp2[f'design_size{idx}'] = df_tmp2[f'design_size{idx}'].astype(float)
            df = pd.concat([df, df_tmp2], axis=1)
        df = df.replace('--', np.nan)

        return df

