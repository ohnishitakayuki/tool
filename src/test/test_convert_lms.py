import os
import sys
from pathlib import Path
import pandas as pd

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.getdf.convert_lms import ConvertLms


# 比較用ファイル作成用
# def test_make_pickle():
#     p = Path('./test_data/data_convert_lms/20231018QC_Global_v3000.000.lms')
#     t = ConvertLms(p)
#     df = t.df(calc='gpos')
#     df.to_pickle('df_gpos.pkl')
#     print(t.df(calc='gpos'))
#     assert 1 == 1

@pytest.mark.parametrize(
        'f, calc, df_pkl',
    [
        ('/test_data/data_convert_lms/20231018QC_Global_v3000.000.lms',
         'gpos',
         '/test_data/data_convert_lms/df_gpos.pkl'),
        ('/test_data/data_convert_lms/20231018QC_Global_v3000.000.lms',
         'simple',
         '/test_data/data_convert_lms/df_simple.pkl'),
    ]
)
def test_convert_lms(f, calc, df_pkl):
    p = Path(os.path.dirname(__file__) + f'{f}')
    p_pkl = Path(os.path.dirname(__file__) + f'{df_pkl}')
    t = ConvertLms(p)
    df = t.df(calc=calc)
    df_result = pd.read_pickle(p_pkl)
    check_equal = df.equals(df_result)
    assert check_equal
