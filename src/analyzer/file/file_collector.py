from pathlib import Path
import shutil
import os
from datetime import datetime


class FileCollector:
    def __init__(self, p_from, p_to,
                 sw_tofolder=True, is_newfile=False, is_recursion=True, is_filesize_check=False):
        self.p_from = Path(p_from)
        self.p_to = Path(p_to)
        self.sw_tofolder = sw_tofolder
        self.is_newfile = is_newfile
        self.is_recursion = is_recursion
        self.is_filesize_check = is_filesize_check

    def collect(self, search_word='*'):
        p_org_lasttime = datetime.fromtimestamp(self._get_last_time())
        if self.is_recursion:
            p = list(Path(self.p_from).glob('**/' + search_word))
        else:
            p = list(Path(self.p_from).glob(search_word))
        p.sort()

        i = 0
        for f in p:
            if self.sw_tofolder:
                p_to_f = Path(str(self.p_to) + '/' + str(f.relative_to(self.p_from)))
            else:
                p_to_f = Path(str(self.p_to) + '/' + str(f.name))
            if f.is_dir():
                continue
            if p_to_f.exists():
                # ファイルサイズチェックが入っている場合、同じときはスキップ。
                if self.is_filesize_check:
                    if f.stat().st_size == p_to_f.stat().st_size:
                        print(f'{f} is skipped. File size is same.')
                        continue
                else:
                    print(f'{f} is skipped.')
                continue
            if self.is_newfile:
                print(p_org_lasttime)
                p_org_timestamp = datetime.timestamp(p_org_lasttime)
                if f.stat().st_mtime <= p_org_timestamp:
                    print(f'{f.name} has been skipped because of old file.')
                    continue
            p_to_folder = p_to_f.parent
            if not p_to_folder.is_dir():
                p_to_folder.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, p_to_f)
            i = i + 1
            print(f'{f} has been copied.')
        if i == 0:
            print('There are no copy files.')
        else:
            print(f'Copy is done. File number of copying is {i}.')

    def _get_last_time(self):
        # ファイルの最終時間を取得。
        p_org = list(Path(self.p_from).glob('*'))
        p_org.sort(key=os.path.getmtime, reverse=True)
        if p_org != []:
            p_org_lasttime = p_org[0].stat().st_mtime
        else:
            p_org_lasttime = 0
        return p_org_lasttime


if __name__ == '__main__':
    p_from = '../../test/test_data/data_file_collector/file_org2'
    p_to = '../../test/test_data/data_file_collector/file_to2'
    f = FileCollector(p_from, p_to)
    f.collect()
