import pandas as pd
from pathlib import Path
import subprocess
import codecs


class ConvertLms:
    lms = 'C:/Program Files (x86)/KLA/IPRO/LmsAscii.exe'
    template_file = 'NFT-ALL-EDGES'

    def __init__(self, p):
        p_text = Path(f'{p.parent}/{p.stem}.txt')
        if not (p_text.exists()):
            subprocess.run([self.lms, str(p), "/T=" + self.template_file], capture_output=True)
        with open(p_text, encoding='utf-8', errors='ignore') as f:
            self.f = f.readlines()

    def df(self, calc=''):
        '''
        calc defaultは設定なし
             single: 2点の平均
        '''
        # テキストデータの最初と最後を取得
        data_line = 0
        list_data = []

        for i, line in enumerate(self.f):
            # ヘッダーまで移動
            if '*** Data Table' in line:
                data_line = i + 2
                continue

            # ヘッダー確認
            if data_line == 0 or i < data_line:
                continue

            # 文字列をリスト化
            list_line = line.split(',')
            list_line = list(map(self._list_convert, list_line))

            # カラム検出
            if i == data_line:
                list_column = list_line
                line_num = len(list_line)
                continue

            # データ終了を確認して終了
            if line_num != len(list_line):
                break

            # リスト化
            list_data.append(list_line)

        df = pd.DataFrame(list_data, columns=list_column)

        columns_tmp = []
        for column in df.columns:
            column = column.strip()
            columns_tmp.append(column)
        df.columns = columns_tmp

        if 'Direction' in df.columns:
            df['Direction'] = df['Direction'].str.strip()

        # 測定時間のdatetime化
        df['End Time'] = pd.to_datetime(df['End Time'])

        # 最終列によくわからんものがついているので削除
        df = df.drop(df.columns[[-1]], axis=1)

        # simple時のデータ補正
        if calc == 'simple':
            df['Edge_ave'] = (df['Edge 1'] + df['Edge 2']) / 2
            df['meas_ave'] = df['Edge_ave'] - df['Design Pos']
            df = df[['Design Pos', 'Row', 'Col', 'Direction', 'meas_ave', 'End Time']]
            df_x = df[df['Direction'] == 'X']
            df_y = df[df['Direction'] == 'Y']
            df_x = df_x.rename(columns={'Design Pos': 'designX', 'meas_ave': 'X', 'End Time': 'meas_date'})
            df_y = df_y.rename(columns={'Design Pos': 'designY', 'meas_ave': 'Y'})
            df = pd.merge(df_x, df_y, how='inner', on=['Row', 'Col'])
            df = df[['designX', 'designY', 'Row', 'Col', 'X', 'Y', 'meas_date']]
        elif calc == 'gpos':
            df['Edge_ave1'] = (df['Edge 1'] + df['Edge 8']) / 2
            df['meas_ave1'] = df['Edge_ave1'] - df['Design Pos']
            df['Edge_ave2'] = (df['Edge 3'] + df['Edge 6']) / 2
            df['meas_ave2'] = df['Edge_ave2'] - df['Design Pos']
            df = df[['Design Pos', 'Row', 'Col', 'Direction', 'meas_ave1', 'meas_ave2', 'End Time']]
            df_x = df[df['Direction'] == 'X']
            df_y = df[df['Direction'] == 'Y']
            df_x = df_x.rename(columns={'Design Pos': 'designX', 'meas_ave1': 'X1',
                                        'meas_ave2': 'X2', 'End Time': 'meas_date'})
            df_y = df_y.rename(columns={'Design Pos': 'designY', 'meas_ave1': 'Y1', 'meas_ave2': 'Y2'})
            df = pd.merge(df_x, df_y, how='inner', on=['Row', 'Col'])
            df = df[['designX', 'designY', 'Row', 'Col', 'X1', 'Y1', 'X2', 'Y2', 'meas_date']]
        elif calc == 'lpos':
            df['Edge_ave'] = (df['Edge 1'] + df['Edge 2']) / 2
            df['meas_ave'] = df['Edge_ave'] - df['Design Pos']
            df = df[['Design Pos', 'Row', 'Col', 'SRow', 'SCol', 'Site', 'Field', 'Direction', 'meas_ave', 'End Time']]
            field_num = len(df['Field'].unique())
            df_x = df[df['Direction'] == 'X']
            df_y = df[df['Direction'] == 'Y'].copy()
            df_y['Field'] = df_y['Field'] - int(field_num/2)
            df_x = df_x.rename(columns={'Design Pos': 'designX', 'meas_ave': 'X', 'End Time': 'meas_date'})
            df_y = df_y.rename(columns={'Design Pos': 'designY', 'meas_ave': 'Y'})
            df = pd.merge(df_x, df_y, how='inner', on=['Row', 'Col', 'SRow', 'SCol', 'Site', 'Field'])
            df = df[['designX', 'designY', 'Row', 'Col', 'Site', 'Field', 'X', 'Y', 'meas_date']]
        elif calc == 'sl':
            df['Edge_ave'] = (df['Edge 1'] + df['Edge 2']) / 2
            df['meas_ave'] = df['Edge_ave'] - df['Design Pos']
            df = df[['Design Pos', 'Row', 'Col', 'Direction', 'Site', 'Field', 'meas_ave', 'End Time']]
            df_x = df[df['Direction'] == 'X']
            df_y = df[df['Direction'] == 'Y']
            df_x = df_x.rename(columns={'Design Pos': 'designX', 'meas_ave': 'X', 'End Time': 'meas_date'})
            df_y = df_y.rename(columns={'Design Pos': 'designY', 'meas_ave': 'Y'})
            df = pd.merge(df_x, df_y, how='inner', on=['Row', 'Col', 'Site'])
            df = df[['designX', 'designY', 'Row', 'Col', 'Site', 'X', 'Y', 'meas_date']]
        return df

    def _list_convert(self, x):
        # リストの文字変換用1
        x = x.strip()
        if self._isfloat(x):
            x = float(x)
            if x.is_integer():
                x = int(x)
        return x

    def _isfloat(self, s):  # 浮動小数点数値を表しているかどうかを判定
        # リストの文字変換用2
        try:
            float(s)  # 文字列を実際にfloat関数で変換してみる
        except ValueError:
            return False  # 例外が発生＝変換できないのでFalseを返す
        else:
            return True  # 変換できたのでTrueを返す


if __name__ == '__main__':
    p = Path('../../test/test_data/data_convert_lms/20231018QC_Global_v3000.000.lms')
    t = ConvertLms(p)
    df = t.df(calc='lpos')
    df.to_csv('../../t.csv')
