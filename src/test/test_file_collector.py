import os
import sys
import shutil
import filecmp
import pandas as pd
from pathlib import Path

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from analyzer.file.file_collector import FileCollector


@pytest.fixture()
def data_copy():
    p_to = Path(os.path.dirname(__file__) + '/test_data/data_file_collector/file_to/')
    p_to_org = Path(os.path.dirname(__file__) + '/test_data/data_file_collector/file_to_org/')
    shutil.copytree(p_to_org, p_to)
    yield
    shutil.rmtree(p_to)


def test_data_collection(data_copy):
    p_from = Path(os.path.dirname(__file__) + '/test_data/data_file_collector/file_org/')
    p_to = Path(os.path.dirname(__file__) + '/test_data/data_file_collector/file_to/')
    f = FileCollector(p_from, p_to)
    f.collect('*')

    is_same = True
    for f in p_from.glob('**/*'):
        if f.is_dir():
            continue
        p_to_f = Path(str(p_to) + '/' + str(f.relative_to(p_from)))
        if not(filecmp.cmp(f, p_to_f)):
            is_same = False
            break

    assert is_same


