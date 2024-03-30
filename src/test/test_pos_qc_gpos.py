import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.pos_qc.pos_qc_gpos import PosQcGpos


# # 比較用ファイル作成用
# def test_make_pickle():
#     p_lms1 = Path('./test_data/data_pos_qc_gpos/20231018QC_Global_v3000.000.lms')
#     p_lms2 = Path('./test_data/data_pos_qc_gpos/20231018QC_Global_v3000.001.lms')
#     c = PosQcGpos(p_lms1, p_lms2)
#     with open('result_gpos.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert 1 == 1

@pytest.mark.parametrize(
        'p1, p2, p_result',
    [
        ('/test_data/data_pos_qc_gpos/20231018QC_Global_v3000.000.lms',
         '/test_data/data_pos_qc_gpos/20231018QC_Global_v3000.001.lms',
         '/test_data/data_pos_qc_gpos/result_gpos.pkl'),
    ]
)
def test_gpos(p1, p2, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_time_1st', 'meas_start_1st', 'meas_end_1st', 'meas_time_2nd', 'meas_start_2nd', 'meas_end_2nd', ]
    key_value = ['x_3s_s1_nocorr', 'y_3s_s1_nocorr', 'x_3s_s1_rot', 'y_3s_s1_rot', 'x_3s_s1_1st', 'y_3s_s1_1st', 'x_3s_s2_nocorr',
     'y_3s_s2_nocorr', 'x_3s_s2_rot', 'y_3s_s2_rot', 'x_3s_s2_1st', 'y_3s_s2_1st', 'a0_data1_s1', 'b0_data1_s1',
     'a1_data1_s1', 'b1_data1_s1', 'a2_data1_s1', 'b2_data1_s1', 'rot_data1_s1', 'a0_data2_s1', 'b0_data2_s1',
     'a1_data2_s1', 'b1_data2_s1', 'a2_data2_s1', 'b2_data2_s1', 'rot_data2_s1', 'a0_data1_s2', 'b0_data1_s2',
     'a1_data1_s2', 'b1_data1_s2', 'a2_data1_s2', 'b2_data1_s2', 'rot_data1_s2', 'a0_data2_s2', 'b0_data2_s2',
     'a1_data2_s2', 'b1_data2_s2', 'a2_data2_s2', 'b2_data2_s2', 'rot_data2_s2']

    p_lms1 = Path(os.path.dirname(__file__) + f'{p1}')
    p_lms2 = Path(os.path.dirname(__file__) + f'{p2}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = PosQcGpos(p_lms1, p_lms2)
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

    assert is_equal