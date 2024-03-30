import pandas as pd
from pathlib import Path
import subprocess
import codecs


class ConvertLreg:
    template_file = 'NFT-ALL-EDGES'

    def __init__(self, p):
        print(p)
        with open(p, encoding='utf-8', errors='ignore') as f:
            datas = f.readlines()

        is_data = False
        list_meas = []
        for d in datas:
            d_tmp = d.replace('\n', '')
            list_tmp = d_tmp.split(';')
            if list_tmp[0] == 'DesignX':
                list_meas.append(list_tmp)
                is_data = True
                continue
            if not is_data:
                continue
            list_tmp = [float(s) for s in list_tmp]
            list_meas.append(list_tmp)
        self.list_meas = list_meas

    def df(self):
        # テキストデータの最初と最後を取得
        df = pd.DataFrame(self.list_meas[1:], columns=self.list_meas[0])
        df = df.rename(columns={'DesignX': 'designX', 'DesignY': 'designY', 'DeviationX': 'X', 'DeviationY': 'Y'})

        # umなのでnmに変換
        df['designX'] = df['designX'] * 1000
        df['designY'] = df['designY'] * 1000
        df['X'] = df['X'] * 1000
        df['Y'] = df['Y'] * 1000

        return df


if __name__ == '__main__':
    p = Path('../../test/test_data/data_pos_qc_lreg/QC_Local_CH240_V03-000.010.lms.LocalRegistration.M.0.8.8._._.lreg')
    t = ConvertLreg(p)
    print(t.df())

