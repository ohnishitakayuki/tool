import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.pos_qc.pos_qc_spc import PosQcSpc


# # 比較用ファイル作成用
# def test_make_pickle():
#     p_baseline = Path('./test_data/data_pos_qc_spc/baseline')
#     p = Path('./test_data/data_pos_qc_spc/data')
#     list_p_baseline = list(p_baseline.glob('*.lms'))
#     list_p = list(p.glob('*.lms'))
#     c = PosQcSpc(list_p_baseline, list_p)
#     with open('test_data/data_pos_qc_spc/result_spc.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True

@pytest.mark.parametrize(
        'p_baseline, p, p_result',
    [
        ('/test_data/data_pos_qc_spc/baseline',
         '/test_data/data_pos_qc_spc/data',
         '/test_data/data_pos_qc_spc/result_spc.pkl'),
    ]
)
def test_spc(p_baseline, p, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_start', 'meas_end', 'meas_time']
    key_value = ['x_spc_data1_nocorr', 'y_spc_data1_nocorr', 'x_spc_data1_rot', 'y_spc_data1_rot',
                 'x_spc_data1_1st', 'y_spc_data1_1st', 'x_spc_data2_nocorr', 'y_spc_data2_nocorr',
                 'x_spc_data2_rot', 'y_spc_data2_rot', 'x_spc_data2_1st', 'y_spc_data2_1st',
                 'x_spc_data3_nocorr', 'y_spc_data3_nocorr', 'x_spc_data3_rot', 'y_spc_data3_rot',
                 'x_spc_data3_1st', 'y_spc_data3_1st', 'x_spc_nocorr_max', 'y_spc_nocorr_max',
                 'x_spc_rot_max', 'y_spc_rot_max', 'x_spc_1st_max', 'y_spc_1st_max']

    p_baseline = Path(os.path.dirname(__file__) + f'{p_baseline}')
    p = Path(os.path.dirname(__file__) + f'{p}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    list_p_baseline = list(p_baseline.glob('*.lms'))
    list_p = list(p.glob('*.lms'))
    c = PosQcSpc(list_p_baseline, list_p)
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