import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.pos_qc.pos_qc_lreg import PosQcLreg


# # 比較用ファイル作成用
# def test_make_pickle():
#     p1 = Path('./test_data/data_pos_qc_lreg/QC_Local_CH240_V03-000.010.lms.LocalRegistration.M.0.8.8._._.lreg')
#     p2 = Path('./test_data/data_pos_qc_lreg/QC_Local_CH240_V03-000.011.lms.LocalRegistration.M.0.8.8._._.lreg')
#
#     c = PosQcLreg(p1, p2)
#     with open('test_data/data_pos_qc_lreg/result_lreg.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True

@pytest.mark.parametrize(
        'p1, p2, p_result',
    [
        ('/test_data/data_pos_qc_lreg/QC_Local_CH240_V03-000.010.lms.LocalRegistration.M.0.8.8._._.lreg',
         '/test_data/data_pos_qc_lreg/QC_Local_CH240_V03-000.011.lms.LocalRegistration.M.0.8.8._._.lreg',
         '/test_data/data_pos_qc_lreg/result_lreg.pkl'),
    ]
)
def test_lreg(p1, p2, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_start_1st', 'meas_start_2nd', ]
    key_value = ['x_3s_nocorr', 'y_3s_nocorr',
     'x_3s_rot', 'y_3s_rot', 'x_3s_1st', 'y_3s_1st', 'a0_data1', 'b0_data1', 'a1_data1', 'b1_data1', 'a2_data1',
     'b2_data1', 'rot_data1', 'a0_data2', 'b0_data2', 'a1_data2', 'b1_data2', 'a2_data2', 'b2_data2', 'rot_data2']

    p1 = Path(os.path.dirname(__file__) + f'{p1}')
    p2 = Path(os.path.dirname(__file__) + f'{p2}')

    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = PosQcLreg(p1, p2)
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