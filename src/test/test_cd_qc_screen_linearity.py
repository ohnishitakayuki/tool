import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd_qc.cd_qc_screen_linearity import CdQcScreenLinearity

#
# # 比較用ファイル作成用
# def test_make_pickle():
#     p = Path('./test_data/data_cd_qc_screen_linearity/Screen Linearity_20231202123056.csv')
#     c = CdQcScreenLinearity(p)
#     with open('test_data/data_cd_qc_screen_linearity/result.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True


@pytest.mark.parametrize(
        'p, p_result',
    [
        ('/test_data/data_cd_qc_screen_linearity/Screen Linearity_20231202123056.csv',
         '/test_data/data_cd_qc_screen_linearity/result.pkl'),
    ]
)
def test_screen_linearity(p, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_start', 'meas_end', 'meas_time']
    key_value = ['screen_linearity_hor', 'screen_linearity_ver',]

    p = Path(os.path.dirname(__file__) + f'{p}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = CdQcScreenLinearity(p)
    v = vars(c)
    with open(p_pkl, 'rb') as f:
        v_result = pickle.load(f)
    is_equal = True

    # 時間系、そのまま比較
    print(v_result)
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