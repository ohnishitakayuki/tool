import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd_qc.cd_qc_dynamic_short import CdQcDynamicShort

#
# # 比較用ファイル作成用
# def test_make_pickle():
#     p = Path('./test_data/data_cd_qc_dynamic_short/Dynamic Short AT_20221118133357.csv')
#     c = CdQcDynamicShort(p)
#     with open('test_data/data_cd_qc_dynamic_short/result.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True
#

@pytest.mark.parametrize(
        'p, p_result',
    [
        ('/test_data/data_cd_qc_dynamic_short/Dynamic Short AT_20221118133357.csv',
         '/test_data/data_cd_qc_dynamic_short/result.pkl'),
    ]
)
def test_dynamic_short(p, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_start', 'meas_end', 'meas_time']
    key_value = ['rep_3s_raw', 'rep_3s_1st', 'slope_average', 'rep_3s_raw_chip_1', 'rep_3s_1st_chip_1',
                 'rep_3s_raw_chip_2', 'rep_3s_1st_chip_2', 'rep_3s_raw_chip_3', 'rep_3s_1st_chip_3',
                 'rep_3s_raw_chip_4', 'rep_3s_1st_chip_4', 'rep_3s_raw_chip_5', 'rep_3s_1st_chip_5',
                 'rep_3s_raw_size_80', 'rep_3s_1st_size_80', 'rep_3s_raw_size_100', 'rep_3s_1st_size_100',
                 'rep_3s_raw_size_200', 'rep_3s_1st_size_200', 'rep_3s_raw_size_400', 'rep_3s_1st_size_400',
                 'rep_3s_raw_size_750', 'rep_3s_1st_size_750', 'rep_3s_raw_category_iso_space',
                 'rep_3s_1st_category_iso_space', 'rep_3s_raw_category_iso_line',
                 'rep_3s_1st_category_iso_line', 'rep_3s_raw_category_ls_space',
                 'rep_3s_1st_category_ls_space', 'rep_3s_raw_category_ls_line', 'rep_3s_1st_category_ls_line',
                 'rep_3s_raw_rotation_x', 'rep_3s_1st_rotation_x', 'rep_3s_raw_rotation_y', 'rep_3s_1st_rotation_y',
                 'cd_mean_x_iso_space_80_chip1', 'cd_mean_x_iso_space_80_chip2',
                 'cd_mean_x_iso_space_80_chip3', 'cd_mean_x_iso_space_80_chip4',
                 'cd_mean_x_iso_space_80_chip5', 'cd_mean_x_iso_space_100_chip1',
                 'cd_mean_x_iso_space_100_chip2', 'cd_mean_x_iso_space_100_chip3',
                 'cd_mean_x_iso_space_100_chip4', 'cd_mean_x_iso_space_100_chip5',
                 'cd_mean_x_iso_space_200_chip1', 'cd_mean_x_iso_space_200_chip2',
                 'cd_mean_x_iso_space_200_chip3', 'cd_mean_x_iso_space_200_chip4',
                 'cd_mean_x_iso_space_200_chip5', 'cd_mean_x_iso_space_400_chip1',
                 'cd_mean_x_iso_space_400_chip2', 'cd_mean_x_iso_space_400_chip3',
                 'cd_mean_x_iso_space_400_chip4', 'cd_mean_x_iso_space_400_chip5',
                 'cd_mean_x_iso_space_750_chip1', 'cd_mean_x_iso_space_750_chip2',
                 'cd_mean_x_iso_space_750_chip3', 'cd_mean_x_iso_space_750_chip4',
                 'cd_mean_x_iso_space_750_chip5', 'cd_mean_x_iso_line_80_chip1',
                 'cd_mean_x_iso_line_80_chip2', 'cd_mean_x_iso_line_80_chip3',
                 'cd_mean_x_iso_line_80_chip4', 'cd_mean_x_iso_line_80_chip5',
                 'cd_mean_x_iso_line_100_chip1', 'cd_mean_x_iso_line_100_chip2',
                 'cd_mean_x_iso_line_100_chip3', 'cd_mean_x_iso_line_100_chip4',
                 'cd_mean_x_iso_line_100_chip5', 'cd_mean_x_iso_line_200_chip1',
                 'cd_mean_x_iso_line_200_chip2', 'cd_mean_x_iso_line_200_chip3',
                 'cd_mean_x_iso_line_200_chip4', 'cd_mean_x_iso_line_200_chip5',
                 'cd_mean_x_iso_line_400_chip1', 'cd_mean_x_iso_line_400_chip2',
                 'cd_mean_x_iso_line_400_chip3', 'cd_mean_x_iso_line_400_chip4',
                 'cd_mean_x_iso_line_400_chip5', 'cd_mean_x_iso_line_750_chip1',
                 'cd_mean_x_iso_line_750_chip2', 'cd_mean_x_iso_line_750_chip3',
                 'cd_mean_x_iso_line_750_chip4', 'cd_mean_x_iso_line_750_chip5',
                 'cd_mean_x_ls_space_80_chip1', 'cd_mean_x_ls_space_80_chip2', 'cd_mean_x_ls_space_80_chip3',
                 'cd_mean_x_ls_space_80_chip4', 'cd_mean_x_ls_space_80_chip5', 'cd_mean_x_ls_space_100_chip1',
                 'cd_mean_x_ls_space_100_chip2', 'cd_mean_x_ls_space_100_chip3', 'cd_mean_x_ls_space_100_chip4',
                 'cd_mean_x_ls_space_100_chip5', 'cd_mean_x_ls_space_200_chip1', 'cd_mean_x_ls_space_200_chip2',
                 'cd_mean_x_ls_space_200_chip3', 'cd_mean_x_ls_space_200_chip4', 'cd_mean_x_ls_space_200_chip5',
                 'cd_mean_x_ls_space_400_chip1', 'cd_mean_x_ls_space_400_chip2', 'cd_mean_x_ls_space_400_chip3',
                 'cd_mean_x_ls_space_400_chip4', 'cd_mean_x_ls_space_400_chip5', 'cd_mean_x_ls_space_750_chip1',
                 'cd_mean_x_ls_space_750_chip2', 'cd_mean_x_ls_space_750_chip3', 'cd_mean_x_ls_space_750_chip4',
                 'cd_mean_x_ls_space_750_chip5', 'cd_mean_x_ls_line_80_chip1', 'cd_mean_x_ls_line_80_chip2',
                 'cd_mean_x_ls_line_80_chip3', 'cd_mean_x_ls_line_80_chip4', 'cd_mean_x_ls_line_80_chip5',
                 'cd_mean_x_ls_line_100_chip1', 'cd_mean_x_ls_line_100_chip2', 'cd_mean_x_ls_line_100_chip3',
                 'cd_mean_x_ls_line_100_chip4', 'cd_mean_x_ls_line_100_chip5', 'cd_mean_x_ls_line_200_chip1',
                 'cd_mean_x_ls_line_200_chip2', 'cd_mean_x_ls_line_200_chip3', 'cd_mean_x_ls_line_200_chip4',
                 'cd_mean_x_ls_line_200_chip5', 'cd_mean_x_ls_line_400_chip1', 'cd_mean_x_ls_line_400_chip2',
                 'cd_mean_x_ls_line_400_chip3', 'cd_mean_x_ls_line_400_chip4', 'cd_mean_x_ls_line_400_chip5',
                 'cd_mean_x_ls_line_750_chip1', 'cd_mean_x_ls_line_750_chip2', 'cd_mean_x_ls_line_750_chip3',
                 'cd_mean_x_ls_line_750_chip4', 'cd_mean_x_ls_line_750_chip5', 'cd_mean_y_iso_space_80_chip1',
                 'cd_mean_y_iso_space_80_chip2', 'cd_mean_y_iso_space_80_chip3',
                 'cd_mean_y_iso_space_80_chip4', 'cd_mean_y_iso_space_80_chip5',
                 'cd_mean_y_iso_space_100_chip1', 'cd_mean_y_iso_space_100_chip2',
                 'cd_mean_y_iso_space_100_chip3', 'cd_mean_y_iso_space_100_chip4',
                 'cd_mean_y_iso_space_100_chip5', 'cd_mean_y_iso_space_200_chip1',
                 'cd_mean_y_iso_space_200_chip2', 'cd_mean_y_iso_space_200_chip3',
                 'cd_mean_y_iso_space_200_chip4', 'cd_mean_y_iso_space_200_chip5',
                 'cd_mean_y_iso_space_400_chip1', 'cd_mean_y_iso_space_400_chip2',
                 'cd_mean_y_iso_space_400_chip3', 'cd_mean_y_iso_space_400_chip4',
                 'cd_mean_y_iso_space_400_chip5', 'cd_mean_y_iso_space_750_chip1',
                 'cd_mean_y_iso_space_750_chip2', 'cd_mean_y_iso_space_750_chip3',
                 'cd_mean_y_iso_space_750_chip4', 'cd_mean_y_iso_space_750_chip5',
                 'cd_mean_y_iso_line_80_chip1', 'cd_mean_y_iso_line_80_chip2',
                 'cd_mean_y_iso_line_80_chip3', 'cd_mean_y_iso_line_80_chip4',
                 'cd_mean_y_iso_line_80_chip5', 'cd_mean_y_iso_line_100_chip1',
                 'cd_mean_y_iso_line_100_chip2', 'cd_mean_y_iso_line_100_chip3',
                 'cd_mean_y_iso_line_100_chip4', 'cd_mean_y_iso_line_100_chip5',
                 'cd_mean_y_iso_line_200_chip1', 'cd_mean_y_iso_line_200_chip2',
                 'cd_mean_y_iso_line_200_chip3', 'cd_mean_y_iso_line_200_chip4',
                 'cd_mean_y_iso_line_200_chip5', 'cd_mean_y_iso_line_400_chip1',
                 'cd_mean_y_iso_line_400_chip2', 'cd_mean_y_iso_line_400_chip3',
                 'cd_mean_y_iso_line_400_chip4', 'cd_mean_y_iso_line_400_chip5',
                 'cd_mean_y_iso_line_750_chip1', 'cd_mean_y_iso_line_750_chip2',
                 'cd_mean_y_iso_line_750_chip3', 'cd_mean_y_iso_line_750_chip4',
                 'cd_mean_y_iso_line_750_chip5', 'cd_mean_y_ls_space_80_chip1',
                 'cd_mean_y_ls_space_80_chip2', 'cd_mean_y_ls_space_80_chip3', 'cd_mean_y_ls_space_80_chip4',
                 'cd_mean_y_ls_space_80_chip5', 'cd_mean_y_ls_space_100_chip1', 'cd_mean_y_ls_space_100_chip2',
                 'cd_mean_y_ls_space_100_chip3', 'cd_mean_y_ls_space_100_chip4', 'cd_mean_y_ls_space_100_chip5',
                 'cd_mean_y_ls_space_200_chip1', 'cd_mean_y_ls_space_200_chip2', 'cd_mean_y_ls_space_200_chip3',
                 'cd_mean_y_ls_space_200_chip4', 'cd_mean_y_ls_space_200_chip5', 'cd_mean_y_ls_space_400_chip1',
                 'cd_mean_y_ls_space_400_chip2', 'cd_mean_y_ls_space_400_chip3', 'cd_mean_y_ls_space_400_chip4',
                 'cd_mean_y_ls_space_400_chip5', 'cd_mean_y_ls_space_750_chip1', 'cd_mean_y_ls_space_750_chip2',
                 'cd_mean_y_ls_space_750_chip3', 'cd_mean_y_ls_space_750_chip4', 'cd_mean_y_ls_space_750_chip5',
                 'cd_mean_y_ls_line_80_chip1', 'cd_mean_y_ls_line_80_chip2', 'cd_mean_y_ls_line_80_chip3',
                 'cd_mean_y_ls_line_80_chip4', 'cd_mean_y_ls_line_80_chip5', 'cd_mean_y_ls_line_100_chip1',
                 'cd_mean_y_ls_line_100_chip2', 'cd_mean_y_ls_line_100_chip3', 'cd_mean_y_ls_line_100_chip4',
                 'cd_mean_y_ls_line_100_chip5', 'cd_mean_y_ls_line_200_chip1', 'cd_mean_y_ls_line_200_chip2',
                 'cd_mean_y_ls_line_200_chip3', 'cd_mean_y_ls_line_200_chip4', 'cd_mean_y_ls_line_200_chip5',
                 'cd_mean_y_ls_line_400_chip1', 'cd_mean_y_ls_line_400_chip2', 'cd_mean_y_ls_line_400_chip3',
                 'cd_mean_y_ls_line_400_chip4', 'cd_mean_y_ls_line_400_chip5', 'cd_mean_y_ls_line_750_chip1',
                 'cd_mean_y_ls_line_750_chip2', 'cd_mean_y_ls_line_750_chip3', 'cd_mean_y_ls_line_750_chip4',
                 'cd_mean_y_ls_line_750_chip5', 'column_num', 'row_num',]

    p = Path(os.path.dirname(__file__) + f'{p}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = CdQcDynamicShort(p)
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