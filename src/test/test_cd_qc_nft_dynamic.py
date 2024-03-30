import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd_qc.cd_qc_nft_dynamic import CdQcNftDynamic


# # 比較用ファイル作成用
# def test_make_pickle():
#     p = Path('./test_data/data_cd_qc_nft_dynamic_trend/NFT Dynamic_20231220102342.csv')
#     c = CdQcNftDynamic(p)
#     with open('test_data/data_cd_qc_nft_dynamic_trend/result_nft_dynamic.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True


@pytest.mark.parametrize(
        'p, p_result',
    [
        ('/test_data/data_cd_qc_nft_dynamic_trend/NFT Dynamic_20231220102342.csv',
         '/test_data/data_cd_qc_nft_dynamic_trend/result_nft_dynamic.pkl'),
    ]
)
def test_sl(p, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_start', 'meas_end', 'meas_time']
    key_value = ['rep_3s_hor_space', 'slope_1st_line_hor_space', 'slope_2nd_line_hor_space',
                 'diff_mean_hor_space', 'cd_mean_1st_hor_space', 'cd_mean_2nd_hor_space', 'cd_3s_1st_hor_space',
                 'cd_3s_2nd_hor_space', 'cd_max_1st_hor_space', 'cd_max_2nd_hor_space', 'cd_min_1st_hor_space',
                 'cd_min_2nd_hor_space', 'cd_range_1st_hor_space', 'cd_range_2nd_hor_space', 'rep_3s_ver_space',
                 'slope_1st_line_ver_space', 'slope_2nd_line_ver_space', 'diff_mean_ver_space',
                 'cd_mean_1st_ver_space', 'cd_mean_2nd_ver_space', 'cd_3s_1st_ver_space', 'cd_3s_2nd_ver_space',
                 'cd_max_1st_ver_space', 'cd_max_2nd_ver_space', 'cd_min_1st_ver_space', 'cd_min_2nd_ver_space',
                 'cd_range_1st_ver_space', 'cd_range_2nd_ver_space', 'rep_3s_hor_pitch', 'slope_1st_line_hor_pitch',
                 'slope_2nd_line_hor_pitch', 'diff_mean_hor_pitch',
                 'cd_mean_1st_hor_pitch', 'cd_mean_2nd_hor_pitch', 'cd_3s_1st_hor_pitch', 'cd_3s_2nd_hor_pitch',
                 'cd_max_1st_hor_pitch', 'cd_max_2nd_hor_pitch', 'cd_min_1st_hor_pitch', 'cd_min_2nd_hor_pitch',
                 'cd_range_1st_hor_pitch', 'cd_range_2nd_hor_pitch', 'rep_3s_ver_pitch', 'slope_1st_line_ver_pitch',
                 'slope_2nd_line_ver_pitch', 'diff_mean_ver_pitch', 'cd_mean_1st_ver_pitch', 'cd_mean_2nd_ver_pitch',
                 'cd_3s_1st_ver_pitch', 'cd_3s_2nd_ver_pitch', 'cd_max_1st_ver_pitch', 'cd_max_2nd_ver_pitch',
                 'cd_min_1st_ver_pitch', 'cd_min_2nd_ver_pitch', 'cd_range_1st_ver_pitch', 'cd_range_2nd_ver_pitch']

    p = Path(os.path.dirname(__file__) + f'{p}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = CdQcNftDynamic(p)
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