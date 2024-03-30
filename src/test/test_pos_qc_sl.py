import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.pos_qc.pos_qc_sl import PosQcSl


# # 比較用ファイル作成用
# def test_make_pickle():
#     p = Path('./test_data/data_pos_qc_sl/QC_Screen_Linearity_V03-000.010.lms')
#     c = PosQcSl(p)
#     with open('test_data/data_pos_qc_sl/result_sl.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True
# #
@pytest.mark.parametrize(
        'p, p_result',
    [
        ('/test_data/data_pos_qc_sl/QC_Screen_Linearity_V03-000.010.lms',
         '/test_data/data_pos_qc_sl/result_sl.pkl'),
    ]
)
def test_sl(p, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_start', 'meas_end', 'meas_time']
    key_value = ['x_3s_nocorr', 'y_3s_nocorr', 'x_max_nocorr', 'x_min_nocorr', 'x_range_nocorr',
                'y_3s_nocorr', 'y_mean_nocorr', 'y_max_nocorr', 'y_min_nocorr', 'y_range_nocorr',
                'x_3s_shift', 'y_3s_shift', 'x_max_shift', 'x_min_shift', 'x_range_shift',
                'y_3s_shift', 'y_mean_shift', 'y_max_shift', 'y_min_shift', 'y_range_shift',]

    p = Path(os.path.dirname(__file__) + f'{p}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = PosQcSl(p)
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