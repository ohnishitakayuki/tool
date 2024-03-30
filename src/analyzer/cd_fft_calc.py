import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import signal

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from cd.cd_fft import CDFft

class CdFftCalc:
    min_graph = 0.00000000000001

    def __init__(self, p_list, edge_type, averaged=True, pixel=None):
        self.averaged = averaged

        if edge_type == 'edge_left':
            self.edge_name = 'Edge Left'
        elif edge_type == 'edge_right':
            self.edge_name = 'Edge Right'
        elif edge_type == 'lwr':
            self.edge_name = 'LWR'
        df = pd.DataFrame()

        for i, f_str in enumerate(p_list):
            f = Path(f_str)
            print(i + 1, f)
            v = CDFft(f)
            df_tmp = v.df_fft(pixel, edge_type)
            df_tmp['name'] = f.name
            df = pd.concat([df, df_tmp])
        self.idx = i + 1
        self.df = df
        if averaged:
            self.df_all = df.groupby('freq').agg({'pow': 'mean'}).reset_index()
        else:
            self.df_all = df.pivot(index='freq', columns='name', values='pow')

    def graph(self, p_save=''):
        # 10/5 平均出ないときの扱いを考えよう
        df = self.df_all
        fig, ax = plt.subplots()
        if self.averaged:
            df = df[df['pow'] > self.min_graph]
            ax.plot(df['freq'], df['pow'])
        else:
            for c in df.columns.values:
                if not 'csv' in c:
                    continue
                df_tmp = df[df[c] > self.min_graph]
                ax.plot(df_tmp.index, df_tmp[c])
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title(f'{self.edge_name} Spatial Frequency')
        ax.set_xlabel('Spatial Frequency [1/nm]')
        ax.set_ylabel('Density of Power Spectrum [nm$^{2}$]')
        if not(p_save):
            return fig, ax
        else:
            plt.savefig(p_save)

if __name__ == '__main__':
    p = Path('../test/test_data/data_cd_fft/')
    list_p = list(p.glob('*.csv'))
    t = CdFftCalc(list_p, 'edge_left', False, None)
    print(t.graph())
