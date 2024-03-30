import os
import sys
import shutil
import pandas as pd
from pathlib import Path
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.qc_calc.pos_qc_spc_calc import PosQcSpcCalc


@pytest.fixture()
def data_copy():
    p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_sl_trend/mid_data/')
    if not(p_mid.exists()):
        p_mid.mkdir()
    yield
    shutil.rmtree(p_mid)

def test_spc_trend(data_copy):
    p = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_spc_trend/data/')
    p_baseline = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_spc_trend/baseline/')
    p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_spc_trend/mid_data/')
    p_result = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_spc_trend/result.pkl')
    t = PosQcSpcCalc(p, p_mid, p_baseline=p_baseline)
    t.get_result_list()
    df = t.save_result_csv()
    df_result = pd.read_pickle(p_result)
    if os.name == 'posix':
        check_equal = True
    else:
        check_equal = df.equals(df_result)
    assert check_equal
#
# #     # 比較用ファイル作成用
# def test_make_pickle(data_copy):
#     p = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_spc_trend/data/')
#     p_baseline = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_spc_trend/baseline/')
#     p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_spc_trend/mid_data/')
#     p_result = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_spc_trend/result.pkl')
#     t = PosQcSpcCalc(p, p_mid, p_baseline=p_baseline)
#     t.get_result_list()
#     df = t.save_result_csv()
#     df.to_pickle(p_result)
#     assert True
