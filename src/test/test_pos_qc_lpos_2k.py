import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.pos_qc.pos_qc_lpos_2k import PosQcLpos2k


# # # 比較用ファイル作成用
# def test_make_pickle_symmetry():
#     p1 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_16-51-10.prx')
#     p2 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_17-03-53.prx')
#     p_sl0_1 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-44-25.prx')
#     p_sl0_2 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_16-48-01.prx')
#     p_sl1_1 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-57-14.prx')
#     p_sl1_2 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-00-48.prx')
#     p_sl2_1 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_17-10-01.prx')
#     p_sl2_2 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-13-33.prx')
#     c = PosQcLpos2k(p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2)
#     with open('test_data/data_pos_qc_lpos_2k/result_lpos_symmetry.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True
#  # 比較用ファイル作成用 symmetry
# def test_make_pickle_threshold():
#     p1 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_16-51-10.prx')
#     p2 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_17-03-53.prx')
#     p_sl0_1 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-44-25.prx')
#     p_sl0_2 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_16-48-01.prx')
#     p_sl1_1 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-57-14.prx')
#     p_sl1_2 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-00-48.prx')
#     p_sl2_1 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_17-10-01.prx')
#     p_sl2_2 = Path('./test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-13-33.prx')
#     c = PosQcLpos2k(p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2, calc='lpos_threshold')
#     with open('test_data/data_pos_qc_lpos_2k/result_lpos_threshold.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True

@pytest.mark.parametrize(
        'p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2, p_result',
    [
        ('/test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_16-51-10.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_17-03-53.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-44-25.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_16-48-01.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-57-14.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-00-48.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_17-10-01.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-13-33.prx',
         '/test_data/data_pos_qc_lpos_2k/result_lpos_symmetry.pkl'),
    ]
)
def test_lpos2k_symmetry(p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_time_1st', 'meas_start_1st', 'meas_end_1st', 'meas_time_2nd', 'meas_start_2nd', 'meas_end_2nd', ]
    key_value = ['x_3s_nocorr', 'y_3s_nocorr',
     'x_3s_rot', 'y_3s_rot', 'x_3s_1st', 'y_3s_1st', 'a0_data1', 'b0_data1', 'a1_data1', 'b1_data1', 'a2_data1',
     'b2_data1', 'rot_data1', 'a0_data2', 'b0_data2', 'a1_data2', 'b1_data2', 'a2_data2', 'b2_data2', 'rot_data2']

    p1 = Path(os.path.dirname(__file__) + f'{p1}')
    p2 = Path(os.path.dirname(__file__) + f'{p2}')
    p_sl0_1 = Path(os.path.dirname(__file__) + f'{p_sl0_1}')
    p_sl0_2 = Path(os.path.dirname(__file__) + f'{p_sl0_2}')
    p_sl1_1 = Path(os.path.dirname(__file__) + f'{p_sl1_1}')
    p_sl1_2 = Path(os.path.dirname(__file__) + f'{p_sl1_2}')
    p_sl2_1 = Path(os.path.dirname(__file__) + f'{p_sl2_1}')
    p_sl2_2 = Path(os.path.dirname(__file__) + f'{p_sl2_2}')

    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = PosQcLpos2k(p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2)
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

@pytest.mark.parametrize(
        'p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2, p_result',
    [
        ('/test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_16-51-10.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35_N5_MB_B_2024-07-24_1_17-03-53.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-44-25.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_16-48-01.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-57-14.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-00-48.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_17-10-01.prx',
         '/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_2_17-13-33.prx',
         '/test_data/data_pos_qc_lpos_2k/result_lpos_threshold.pkl'),
    ]
)
def test_lpos2k_threshold(p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_time_1st', 'meas_start_1st', 'meas_end_1st', 'meas_time_2nd', 'meas_start_2nd', 'meas_end_2nd', ]
    key_value = ['x_3s_nocorr', 'y_3s_nocorr',
     'x_3s_rot', 'y_3s_rot', 'x_3s_1st', 'y_3s_1st', 'a0_data1', 'b0_data1', 'a1_data1', 'b1_data1', 'a2_data1',
     'b2_data1', 'rot_data1', 'a0_data2', 'b0_data2', 'a1_data2', 'b1_data2', 'a2_data2', 'b2_data2', 'rot_data2']

    p1 = Path(os.path.dirname(__file__) + f'{p1}')
    p2 = Path(os.path.dirname(__file__) + f'{p2}')
    p_sl0_1 = Path(os.path.dirname(__file__) + f'{p_sl0_1}')
    p_sl0_2 = Path(os.path.dirname(__file__) + f'{p_sl0_2}')
    p_sl1_1 = Path(os.path.dirname(__file__) + f'{p_sl1_1}')
    p_sl1_2 = Path(os.path.dirname(__file__) + f'{p_sl1_2}')
    p_sl2_1 = Path(os.path.dirname(__file__) + f'{p_sl2_1}')
    p_sl2_2 = Path(os.path.dirname(__file__) + f'{p_sl2_2}')

    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = PosQcLpos2k(p1, p2, p_sl0_1, p_sl0_2, p_sl1_1, p_sl1_2, p_sl2_1, p_sl2_2, calc='lpos_threshold')
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