import os
import sys
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.pos.pos_spc import PosSpc
from analyzer.pos_spc_calc import PosSpcCalc


@pytest.mark.parametrize(
        'f_baseline, f_data, diff_x, diff_y',
    [
        ('/BaseLine/20230331_BaseLine/', '/trend_data/20230912/2023091215x15_SPC_swath_Array_CTDconv.000.002.lms', 0.2921174782872745, 0.3123665177153998,),
    ]
)
def test_spc_1point(f_baseline, f_data, diff_x, diff_y):
    folder_baseline = Path(os.path.dirname(__file__) + f'/test_data/data_ipro8_spc/{f_baseline}')
    path_data = Path(os.path.dirname(__file__) + f'/test_data/data_ipro8_spc/{f_data}')

    search_baseline = '15x15_SPC_swath_Array*lms'
    c = PosSpc(folder_baseline, search_baseline=search_baseline, sw=1)
    c.put_data(str(path_data))
    if c.diff_3s_x == diff_x and c.diff_3s_y == diff_y:
        test_result = True
    else:
        test_result = False
    assert test_result


@pytest.mark.parametrize(
        'p_baseline, p_data, sw, max_meas, p_result',
    [
        ('BaseLine/20230331_BaseLine/', 'trend_data/', 1, 3, 'result_df_all.pkl'),
    ]
)
def test_spc_calc_df_all(p_baseline, p_data, sw, max_meas, p_result):
    path_baseline = Path(os.path.dirname(__file__) + f'/test_data/data_ipro8_spc/{p_baseline}')
    path_data = Path(os.path.dirname(__file__) + f'/test_data/data_ipro8_spc/{p_data}')
    path_result = Path(os.path.dirname(__file__) + f'/test_data/data_ipro8_spc/{p_result}')
    search_baseline = '15x15_SPC_swath_Array*lms'
    search_word = '*15x15_SPC_swath_Array*lms'
    t = PosSpcCalc(path_baseline, path_data, search_baseline, search_word, sw=sw, max_meas=max_meas)
    df_all = t.df_all
    df_result = pd.read_pickle(path_result)
    df_all['3s_x'] = df_all['3s_x'].round(8)
    df_all['3s_y'] = df_all['3s_y'].round(8)
    df_result['3s_x'] = df_result['3s_x'].round(8)
    df_result['3s_y'] = df_result['3s_y'].round(8)
    check_equal = df_all.equals(df_result)
    assert check_equal


@pytest.mark.parametrize(
        'p_baseline, p_data, sw, max_meas, p_result',
    [
        ('BaseLine/20230331_BaseLine/', 'trend_data/', 1, 3, 'result_df_ave.pkl'),
    ]
)
def test_spc_calc_df_ave(p_baseline, p_data, sw, max_meas, p_result):
    path_baseline = Path(os.path.dirname(__file__) + f'/test_data/data_ipro8_spc/{p_baseline}')
    path_data = Path(os.path.dirname(__file__) + f'/test_data/data_ipro8_spc/{p_data}')
    path_result = Path(os.path.dirname(__file__) + f'/test_data/data_ipro8_spc/{p_result}')
    search_baseline = '15x15_SPC_swath_Array*lms'
    search_word = '*15x15_SPC_swath_Array*lms'
    t = PosSpcCalc(path_baseline, path_data, search_baseline, search_word, sw=sw, max_meas=max_meas)
    df_ave = t.df_ave
    df_result = pd.read_pickle(path_result)
    df_ave['3s_x'] = df_ave['3s_x'].round(8)
    df_ave['3s_y'] = df_ave['3s_y'].round(8)
    df_result['3s_x'] = df_result['3s_x'].round(8)
    df_result['3s_y'] = df_result['3s_y'].round(8)
    check_equal = df_ave.equals(df_result)
    assert check_equal

# # 比較用ファイル作成用
# def test_make_pickle():
#     path_baseline = Path(os.path.dirname(__file__) + '/test_data/data_ipro8_spc/BaseLine/20230331_BaseLine/')
#     path_data = Path(os.path.dirname(__file__) + '/test_data/data_ipro8_spc/trend_data/')
#     search_baseline = '15x15_SPC_swath_Array*lms'
#     search_word = '*15x15_SPC_swath_Array*lms'
#     t = PosSpcCalc(path_baseline, path_data, search_baseline, search_word, sw=1, max_meas=3)
#     print(t.df_all)
#     print(t.df_ave)
#     t.df_all.to_pickle('result_df_all.pkl')
#     t.df_ave.to_pickle('result_df_ave.pkl')
#
#     assert 1 == 1
