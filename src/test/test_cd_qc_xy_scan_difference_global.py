import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd_qc.cd_qc_xy_scan_difference_global import CdQcXyScanDifferenceGlobal


# # 比較用ファイル作成用
# def test_make_pickle():
#     p_0 = Path('./test_data/data_cd_qc_xy_scan_difference_global/XY scan difference global R0_20231111205226.csv')
#     p_270 = Path('./test_data/data_cd_qc_xy_scan_difference_global/XY scan difference global R270_20231111213606.csv')
#     c = CdQcXyScanDifferenceGlobal(p_0, p_270)
#     with open('test_data/data_cd_qc_xy_scan_difference_global/result.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True

@pytest.mark.parametrize(
        'p_0deg, p_270deg, p_result',
    [
        ('/test_data/data_cd_qc_xy_scan_difference_global/XY scan difference global R0_20231111205226.csv',
         '/test_data/data_cd_qc_xy_scan_difference_global/XY scan difference global R270_20231111213606.csv',
         '/test_data/data_cd_qc_xy_scan_difference_global/result.pkl'),
    ]
)
def test_sl(p_0deg, p_270deg, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_start_0deg', 'meas_end_0deg', 'meas_time_0deg',
                'meas_start_270deg', 'meas_end_270deg', 'meas_time_270deg', ]
    key_value = ['center_hor_space', 'center_ver_space', 'global_hor_space', 'global_ver_space',
                 'center_hor_pitch', 'center_ver_pitch', 'global_hor_pitch', 'global_ver_pitch',
                 'cd_mean_hor_0deg_pitch', 'cd_mean_hor_0deg_space',
                 'cd_mean_hor_270deg_pitch', 'cd_mean_hor_270deg_space',
                 'cd_mean_ver_0deg_pitch', 'cd_mean_ver_0deg_space',
                 'cd_mean_ver_270deg_pitch', 'cd_mean_ver_270deg_space',
                 'xy_diff_0deg_pitch',
                 'xy_diff_0deg_space',
                 'xy_diff_270deg_pitch',
                 'xy_diff_270deg_space',
                 'xy_scan_diff_hor_pitch_12_1',
                 'xy_scan_diff_hor_pitch_12_12',
                 'xy_scan_diff_hor_pitch_12_6',
                 'xy_scan_diff_hor_pitch_1_1',
                 'xy_scan_diff_hor_pitch_1_12',
                 'xy_scan_diff_hor_pitch_1_6',
                 'xy_scan_diff_hor_pitch_6_1',
                 'xy_scan_diff_hor_pitch_6_12',
                 'xy_scan_diff_hor_pitch_6_6',
                 'xy_scan_diff_hor_space_12_1',
                 'xy_scan_diff_hor_space_12_12',
                 'xy_scan_diff_hor_space_12_6',
                 'xy_scan_diff_hor_space_1_1',
                 'xy_scan_diff_hor_space_1_12',
                 'xy_scan_diff_hor_space_1_6',
                 'xy_scan_diff_hor_space_6_1',
                 'xy_scan_diff_hor_space_6_12',
                 'xy_scan_diff_hor_space_6_6',
                 'xy_scan_diff_ver_pitch_12_1',
                 'xy_scan_diff_ver_pitch_12_12',
                 'xy_scan_diff_ver_pitch_12_6',
                 'xy_scan_diff_ver_pitch_1_1',
                 'xy_scan_diff_ver_pitch_1_12',
                 'xy_scan_diff_ver_pitch_1_6',
                 'xy_scan_diff_ver_pitch_6_1',
                 'xy_scan_diff_ver_pitch_6_12',
                 'xy_scan_diff_ver_pitch_6_6',
                 'xy_scan_diff_ver_space_12_1',
                 'xy_scan_diff_ver_space_12_12',
                 'xy_scan_diff_ver_space_12_6',
                 'xy_scan_diff_ver_space_1_1',
                 'xy_scan_diff_ver_space_1_12',
                 'xy_scan_diff_ver_space_1_6',
                 'xy_scan_diff_ver_space_6_1',
                 'xy_scan_diff_ver_space_6_12',
                 'xy_scan_diff_ver_space_6_6',
                 ]

    p_0deg = Path(os.path.dirname(__file__) + f'{p_0deg}')
    p_270deg = Path(os.path.dirname(__file__) + f'{p_270deg}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = CdQcXyScanDifferenceGlobal(p_0deg, p_270deg)
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
