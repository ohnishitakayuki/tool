import os
import sys
import shutil
import filecmp
import pandas as pd
from pathlib import Path
from datetime import datetime
from datetime import timedelta

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.file.file_deleter import FileDeleter


@pytest.fixture()
def data_copy():
    p_to = Path(os.path.dirname(__file__) + '/test_data/data_file_deleter/data_set/')
    p_to_org = Path(os.path.dirname(__file__) + '/test_data/data_file_deleter/data_set_org/')
    shutil.copytree(p_to_org, p_to)
    yield
    shutil.rmtree(p_to)


def test_data_collection(data_copy):
    p = Path(os.path.dirname(__file__) + '/test_data/data_file_deleter/data_set/')
    p_ref = Path(os.path.dirname(__file__) + '/test_data/data_file_deleter/data_set_ref/')
    p_test = Path(os.path.dirname(__file__) + '/test_data/data_file_deleter/data_set_test/')
    f = FileDeleter(p, p_ref)

    # テスト用削除ファイルの事前計算
    p_file = Path(str(p) + '/NFT_Dynamic_V01_2-9/NFT_Dynamic_V01_2-9.000.A00002009S0001.bmp')
    dt_now = datetime.now()
    dt_file = datetime.fromtimestamp(os.path.getmtime(p_file))
    delta_time = dt_now - dt_file
    delta_time = delta_time + timedelta(seconds=5)
    exts = ['.csv', '.bmp']

    f.delete(delta_time, exts)

    is_same = True

    # 処理した側から確認。
    for f in p.glob('**/*'):
        if f.is_dir():
            continue
        p_to_f = Path(str(p_test) + '/' + str(f.relative_to(p)))
        if not(filecmp.cmp(f, p_to_f)):
            is_same = False
            break

    # テスト側から確認。こうすることで、片方にしかないファイルを洗いだせる。
    for f in p_test.glob('**/*'):
        if f.is_dir():
            continue
        p_to_f = Path(str(p) + '/' + str(f.relative_to(p_test)))
        if not (filecmp.cmp(f, p_to_f)):
            is_same = False
            break

    assert is_same


