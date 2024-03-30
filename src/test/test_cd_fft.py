import os
import sys
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd.cd_fft import CDFft
from analyzer.cd_fft_calc import CdFftCalc


@pytest.mark.parametrize(
        'p, edge_type',
    [
        ('27_ASI_160pA_GLCD_88_256pt_v1_510H_L6.000.A00005005S0001_00.csv', 'edge_left',),
        ('27_ASI_160pA_GLCD_88_256pt_v1_510H_L6.000.A00005005S0001_00.csv', 'edge_right',),
        ('27_ASI_160pA_GLCD_88_256pt_v1_510H_L6.000.A00005005S0001_00.csv', 'lwr',),
    ]
)
def test_compare_from_var(p, edge_type):
    p = Path(os.path.dirname(__file__) + f'/test_data/data_cd_fft/{p}')
    t = CDFft(p)

    df = t.df_fft(512, edge_type)
    p_spectrum = np.round(df['pow'].sum(), 5)

    # 解析直前の生データの分散を取得。ddofは0にする。
    # パワースペクトルの積分と分散は一致する
    p_var = np.round(t.df_fft_row[0].var(ddof=0),5)
    assert p_spectrum == p_var


@pytest.mark.parametrize(
        'p, edge_type, result',
    [
        ('/test_data/data_cd_fft/', 'edge_left', 'result_edge_left.pkl'),
        ('/test_data/data_cd_fft/', 'edge_right', 'result_edge_right.pkl'),
        ('/test_data/data_cd_fft/', 'lwr', 'result_lwr.pkl'),
    ]
)
def test_compare_calc(p, edge_type, result):
    p_data = Path(os.path.dirname(__file__) + f'{p}')
    p_result = Path(os.path.dirname(__file__) + f'{p}/{result}')
    list_p = list(p_data.glob('*.csv'))
    t = CdFftCalc(list_p, edge_type, True, None)
    df_all = t.df_all
    df_result = pd.read_pickle(p_result)

    df_all = df_all.round(8)
    df_result = df_result.round(8)
    check_equal = df_all.equals(df_result)
    assert check_equal



#
# # 比較用ファイル作成用
# def test_make_pickle():
#     p = Path(os.path.dirname(__file__) + '/test_data/data_cd_fft/')
#     list_p = list(p.glob('*.csv'))
#     t = CdFftCalc(list_p, 'lwr', True, None)
#     df_all = t.df_all
#     df_all.to_pickle('result_lwr.pkl')
#     assert 1 == 1