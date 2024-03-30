import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd_qc.cd_qc_xy_scan_difference_category import CdQcXyScanDifferenceCategory


# # 比較用ファイル作成用
# def test_make_pickle():
#     p_0 = Path('./test_data/data_cd_qc_xy_scan_difference_category/XY scan difference category R0_20231202130241.csv')
#     p_270 = Path('./test_data/data_cd_qc_xy_scan_difference_category/XY scan difference category R270_20231202133239.csv')
#     c = CdQcXyScanDifferenceCategory(p_0, p_270)
#     with open('test_data/data_cd_qc_xy_scan_difference_category/result.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True

@pytest.mark.parametrize(
        'p_0deg, p_270deg, p_result',
    [
        ('/test_data/data_cd_qc_xy_scan_difference_category/XY scan difference category R0_20231202130241.csv',
         '/test_data/data_cd_qc_xy_scan_difference_category/XY scan difference category R270_20231202133239.csv',
         '/test_data/data_cd_qc_xy_scan_difference_category/result.pkl'),
    ]
)
def test_xy_scan_difference_category(p_0deg, p_270deg, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_start_0deg', 'meas_end_0deg', 'meas_time_0deg',
                'meas_start_270deg', 'meas_end_270deg', 'meas_time_270deg', ]
    key_value = ['xy_ave', 'xy_bias', 'xy_bias_chip']

    p_0deg = Path(os.path.dirname(__file__) + f'{p_0deg}')
    p_270deg = Path(os.path.dirname(__file__) + f'{p_270deg}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = CdQcXyScanDifferenceCategory(p_0deg, p_270deg)
    v = vars(c)
    with open(p_pkl, 'rb') as f:
        v_result = pickle.load(f)
    is_equal = True

    # 時間系、そのまま比較
    for k in key_meas:
        if not(v[k] == v_result[k]):
            is_equal = False
            print(k, v[k] == v_result[k])

    # パラメータ系、8桁合えばよい。
    for k in key_value:
        if not(np.round(v[k], 8) == np.round(v_result[k], 8)):
            is_equal = False
            print(k, np.round(v[k], 8) == np.round(v_result[k]))

    assert is_equal
