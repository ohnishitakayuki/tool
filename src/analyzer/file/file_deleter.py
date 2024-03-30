import os
from pathlib import Path
from datetime import datetime
from datetime import timedelta


class FileDeleter:
    def __init__(self, p, p_check=''):
        self.p = Path(p)
        # 比較確認のスイッチとパス設定
        if p_check == '':
            self.is_check = False
        else:
            self.is_check = True
            self.p_check = Path(p_check)

    def delete(self, delta_time, exts=[]):
        i = 0
        i_del = 0
        for f in self.p.glob('**/*'):
            i = i + 1
            print(f'check item {i}, delete {i_del}')
            print(f)
            # 削除する対象か確認。
            is_delete_file = self._check_delete_file(f, delta_time, exts)
            if not is_delete_file:
                continue

            # refとの比較
            if self.is_check:
                has_ref_file = self._check_ref_file(f)
                if not has_ref_file:
                    continue

            # 削除
            i_del = i_del + 1
            print(f'{f} is deleted.')
            f.unlink()


    def _check_delete_file(self, f, delta_time, exts):
        # フォルダは対象外
        if f.is_dir():
            return False

        # 対象拡張子以外は除外
        if exts:
            is_ext = False
            for ext in exts:
                if f.suffix == ext:
                    is_ext = True
                    continue
            if not is_ext:
                return False

        # 設定時間より短いものは除外
        dt_now = datetime.now()
        meas_date = datetime.fromtimestamp(os.path.getmtime(f))
        time_diff = dt_now - meas_date
        if time_diff < delta_time:
            return False
        return True

    def _check_ref_file(self, f):
        str_f = str(f)
        str_p = str(self.p)
        str_resolve = str_f.replace(str_p, '')
        str_p_check = str(self.p_check)
        f_check = Path(str_p_check + str_resolve)
        if f_check.exists():
            return True
        else:
            return False

if __name__ == '__main__':
    p = '../../test/test_data/data_file_deleter/data_set_tmp'
    p_check = '../../test/test_data/data_file_deleter/data_set_ref'
    t = FileDeleter(p, p_check)

    # テスト用削除ファイルの事前計算
    p_file = Path('../../test/test_data/data_file_deleter/data_set_tmp/NFT_Dynamic_V01_2-9/NFT_Dynamic_V01_2-9.000.A00002009S0001.bmp')

    dt_now = datetime.now()
    dt_file = datetime.fromtimestamp(os.path.getmtime(p_file))
    delta_time = dt_now - dt_file
    delta_time = delta_time + timedelta(seconds=5)
    exts = ['.csv', '.bmp']
    t.delete(delta_time, exts)
