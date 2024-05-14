import os
import sys
import configparser
from pathlib import Path
from datetime import timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from analyzer.file.file_collector import FileCollector
from analyzer.file.file_deleter import FileDeleter


class CdSemFileCollector:
    def __init__(self, p):
        self.list_path = self._get_config(p)

    def handle(self):
        for dict_p in self.list_path:
            try:
                self._process(dict_p)
            except FileNotFoundError:
                print('パスが存在しないエラー')

    def _process(self, dict_p):
        # 処理部。コレクトとデリートで処理を変えること。
        p_from = Path(dict_p['p_from'])
        p_to = Path(dict_p['p_to'])
        t = FileCollector(p_from, p_to)
        t.collect()

    def _get_config(self, p):
        config_ini = configparser.ConfigParser()
        config_ini.read(p)
        list_path = []
        for section in config_ini.sections():
            list_path.append(dict(config_ini[section]))

        return list_path


class CdSemFileDeleter(CdSemFileCollector):
    def _process(self, dict_p):
        # 処理部。デリートの処理。
        p = Path(dict_p['p'])
        p_check = Path(dict_p['p_check'])
        t = FileDeleter(p, p_check)
        delete_date = timedelta(days=int(dict_p['delete_date']))
        ext = dict_p['ext'].split(',')
        t.delete(delete_date, ext)


if __name__ == '__main__':
    p = Path('e3640_file_delete.ini')
    t = CdSemFileDeleter(p)
    t.handle()
