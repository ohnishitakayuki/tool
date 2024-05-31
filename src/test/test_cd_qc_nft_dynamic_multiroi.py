import os
import sys
import pickle
import numpy as np
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.cd_qc.cd_qc_nft_dynamic_multiroi import CdNftDynamicMultiRoi


# # 比較用ファイル作成用
# def test_make_pickle():
#     p_normal = Path('./test_data/data_cd_qc_nft_dynamic_multiroi/NFT_Dynamic_multiROI_Normal_V01_1-2.000H.csv')
#     p_no_overlap = Path('./test_data/data_cd_qc_nft_dynamic_multiroi/NFT_Dynamic_multiROI_No_overlap_V01_1-2.000H.csv')
#     c = CdNftDynamicMultiRoi(p_normal, p_no_overlap)
#     with open('test_data/data_cd_qc_nft_dynamic_multiroi/result.pkl', 'wb') as f:
#         pickle.dump(vars(c), f)
#     assert True


@pytest.mark.parametrize(
        'p_normal, p_no_overlap, p_result',
    [
        ('/test_data/data_cd_qc_nft_dynamic_multiroi/NFT_Dynamic_multiROI_Normal_V01_1-2.000H.csv',
         '/test_data/data_cd_qc_nft_dynamic_multiroi/NFT_Dynamic_multiROI_No_overlap_V01_1-2.000H.csv',
         '/test_data/data_cd_qc_nft_dynamic_multiroi/result.pkl'),
    ]
)
def test_cd_qc_nft_dynamic_multiroi(p_normal, p_no_overlap, p_result):
    # 比較リスト、新しく追加したい場合は、ここにいれればいい。辞書は作り直し
    key_meas = ['meas_time', 'meas_start', 'meas_end', 'meas_time_normal', 'meas_start_normal',
                'meas_end_normal', 'meas_time_no_overlap',  'meas_start_no_overlap', 'meas_end_no_overlap', ]
    key_value = ['rep_3s_hor', 'rep_3s_ver', 'cd_mean_hor', 'cd_mean_ref_hor', 'cd_mean_ver', 'cd_mean_ref_ver',
                 'cd_3s_hor', 'cd_3s_ref_hor', 'cd_3s_ver', 'cd_3s_ref_ver', 'cd_max_hor', 'cd_max_ref_hor',
                 'cd_max_ver', 'cd_max_ref_ver', 'cd_min_hor', 'cd_min_ref_hor', 'cd_min_ver', 'cd_min_ref_ver',
                 'cd_range_hor', 'cd_range_ref_hor', 'cd_range_ver', 'cd_range_ref_ver',
                 ]

    p_normal = Path(os.path.dirname(__file__) + f'{p_normal}')
    p_no_overlap = Path(os.path.dirname(__file__) + f'{p_no_overlap}')
    p_pkl = Path(os.path.dirname(__file__) + f'{p_result}')
    c = CdNftDynamicMultiRoi(p_normal, p_no_overlap)
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
