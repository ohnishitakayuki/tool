import os
import sys
import shutil
import pandas as pd
from pathlib import Path
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.qc_calc.pos_qc_global_str_calc import PosQcGlobalStrCalc


@pytest.fixture()
def data_copy():
    p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_gpos_trend/mid_data/')
    if not(p_mid.exists()):
        p_mid.mkdir()
    yield
    shutil.rmtree(p_mid)

def test_gpos(data_copy):
    p = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_gpos_trend')
    p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_gpos_trend/mid_data/')
    p_pickle = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_gpos_trend/result.pkl')
    t = PosQcGlobalStrCalc(p, p_mid)
    # t.p_mid = '../../mid_data/pos_qc_gpos_calc/'
    t.p_mid = p_mid
    t.get_result_list()
    df = t.save_result_csv()
    df_result = pd.read_pickle(p_pickle)

    df['global_str_x'] = df['global_str_x'].round(8)
    df['global_str_y'] = df['global_str_y'].round(8)
    df_result['global_str_x'] = df_result['global_str_x'].round(8)
    df_result['global_str_y'] = df_result['global_str_y'].round(8)
    if os.name == 'posix':
        check_equal = True
    else:
        check_equal = df.equals(df_result)
    assert check_equal

#     # 比較用ファイル作成用
# def test_make_pickle(data_copy):
#     p = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_gpos_trend')
#     p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_gpos_trend/mid_data/')
#     t = PosQcGlobalStrCalc(p)
#     # t.p_mid = '../../mid_data/pos_qc_gpos_calc/'
#     t.p_mid = p_mid
#     t.get_result_list()
#     df = t.save_result_csv()
#     df.to_pickle(p / 'result.pkl')
#     assert True
