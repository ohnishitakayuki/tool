import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd.cd_angle import CdAngle


# # 比較用ファイル作成用
# def test_make_pickle():
#     p = Path('./test_data/data_cd_angle/MB3000_Angle_88nm_V01_P.000H.csv')
#     c = CdAngle(p)
#     with open('test_data/data_cd_angle/result.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True

@pytest.mark.parametrize(
        'p, p_result',
    [
        ('/test_data/data_cd_angle/MB3000_Angle_88nm_V01_P.000H.csv',
         '/test_data/data_cd_angle/result.pkl'),
    ]
)
def test_cd_angle(p, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_time', 'meas_start', 'meas_end', ]
    key_value = ['xy_cd_diff', 'xy_ler_diff', 'deg45_cd_diff', 'deg45_ler_diff', 'angle_cd_diff',
                 'angle_ler_diff', 'ler_hor', 'ler_m45', 'ler_ver', 'ler_p45',
                 ]

    p = Path(os.path.dirname(__file__) + f'{p}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = CdAngle(p)
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
