import os
import sys
import shutil
import pandas as pd
from pathlib import Path
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.qc_calc.cd_qc_cd_mean_calc import CdQcCdMeanCalc


@pytest.fixture()
def data_copy():
    p_mid = Path(os.path.dirname(__file__) + '/test_data/data_cd_qc_cd_mean/mid_data/')
    if not(p_mid.exists()):
        p_mid.mkdir()
    yield
    shutil.rmtree(p_mid)

def test_cd_mean(data_copy):
    p = Path(os.path.dirname(__file__) + '/test_data/data_cd_qc_cd_mean')
    p_mid = Path(os.path.dirname(__file__) + '/test_data/data_cd_qc_cd_mean/mid_data/')
    p_pickle = Path(os.path.dirname(__file__) + '/test_data/data_cd_qc_cd_mean/result_calc.pkl')
    t = CdQcCdMeanCalc(p, p_mid)
    t.p_mid = p_mid
    t.get_result_list()
    df = t.save_result_csv()
    df_result = pd.read_pickle(p_pickle)
    if os.name == 'posix':
        check_equal = True
    else:
        check_equal = df.equals(df_result)
    assert check_equal

#     # 比較用ファイル作成用
# def test_make_pickle(data_copy):
#     p = Path(os.path.dirname(__file__) + '/test_data/data_cd_qc_cd_mean/')
#     p_mid = Path(os.path.dirname(__file__) + '/test_data/data_cd_qc_cd_mean/mid_data/')
#     t = CdQcCdMeanCalc(p, p_mid)
#     # t.p_mid = '../../mid_data/pos_qc_gpos_calc/'
#     t.p_mid = p_mid
#     t.get_result_list()
#     df = t.save_result_csv()
#     df.to_pickle(p / 'result_calc.pkl')
#     assert True
