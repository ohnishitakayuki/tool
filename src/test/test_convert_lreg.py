import os
import sys
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.getdf.convert_lreg import ConvertLreg


# # 比較用ファイル作成用
# def test_make_pickle():
#     p = Path('./test_data/data_pos_qc_lreg/QC_Local_CH240_V03-000.010.lms.LocalRegistration.M.0.8.8._._.lreg')
#     t = ConvertLreg(p)
#     df = t.df()
#     df.to_pickle('./test_data/data_pos_qc_lreg/df_lreg.pkl')
#     print(t.df())
#     assert True

@pytest.mark.parametrize(
        'f, df_pkl',
    [
        ('/test_data/data_pos_qc_lreg/QC_Local_CH240_V03-000.010.lms.LocalRegistration.M.0.8.8._._.lreg',
         '/test_data/data_pos_qc_lreg/df_lreg.pkl'),
    ]
)
def test_convert_lms(f, df_pkl):
    p = Path(os.path.dirname(__file__) + f'{f}')
    p_pkl = Path(os.path.dirname(__file__) + f'{df_pkl}')
    t = ConvertLreg(p)
    df = t.df()
    df_result = pd.read_pickle(p_pkl)
    check_equal = df.equals(df_result)
    print(df)
    print(df_result)
    assert check_equal
