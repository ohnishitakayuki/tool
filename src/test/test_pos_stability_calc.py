import os
import sys
import pandas as pd
from pathlib import Path

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.pos_stability_calc import PosStabilityCalc


@pytest.fixture(params=[
                (False, 10, 0, 'result0.pkl'),
                (False, 10, 1, 'result1.pkl'),
                (False, 10, 2, 'result2.pkl'),
                (True,  10, 0, 'result3.pkl'),
                (True,  10, 1, 'result4.pkl'),
                (True,  10, 2, 'result5.pkl'),
                ])
def check_equal(request):
    p = Path(os.path.dirname(__file__) + '/test_data/data_pos_stability_calc/')
    t = PosStabilityCalc(p, same_load=request.param[0], average_num=request.param[1], sw=request.param[2])
    df = t.df_stab
    p_result = Path(os.path.dirname(__file__) + f'/test_data/data_pos_stability_calc/{request.param[3]}')
    df_result = pd.read_pickle(p_result)
    df = df.round(8)
    df_result = df_result.round(8)
    check_equal = df.equals(df_result)
    return check_equal


def test_a(check_equal):
    assert check_equal == True


# # 比較用ファイル作成用
# def test_make_pickle():
#     p = Path(os.path.dirname(__file__) + '/test_data/data_pos_stability_calc/')
#     t = PosStabilityCalc(p, same_load=True, average_num=10, sw=2)
#     df = t.df_stab
#     df.to_pickle('result5.pkl')
#     assert 1 == 1
