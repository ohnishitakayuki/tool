import os
import sys
import shutil
import pandas as pd
from pathlib import Path
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.qc_calc.pos_qc_local_lreg_str_ch240nm_calc import PosQcLocalLregStrCH240nmCalc


@pytest.fixture()
def data_copy():
    p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_lreg_trend/mid_data/')
    if not(p_mid.exists()):
        p_mid.mkdir()
    yield
    shutil.rmtree(p_mid)

def test_lpos(data_copy):
    p = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_lreg_trend')
    p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_lreg_trend/mid_data/')
    p_pickle = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_lreg_trend/result.pkl')
    t = PosQcLocalLregStrCH240nmCalc(p, p_mid)
    t.p_mid = p_mid
    t.get_result_list()
    df = t.save_result_csv()
    df_result = pd.read_pickle(p_pickle)
    if os.name == 'posix':
        check_equal = True
    else:
        check_equal = df.equals(df_result)
    assert check_equal
#
#     # 比較用ファイル作成用
# def test_make_pickle(data_copy):
#     p = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_lreg_trend')
#     p_mid = Path(os.path.dirname(__file__) + '/test_data/data_pos_qc_lreg_trend/mid_data/')
#     t = PosQcLocalLregStrCH240nmCalc(p, p_mid)
#     t.p_mid = p_mid
#     t.get_result_list()
#     df = t.save_result_csv()
#     df.to_pickle('./test_data/data_pos_qc_lreg_trend/result.pkl')
#     assert True
