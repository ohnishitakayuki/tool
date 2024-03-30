import os
import sys
import pickle

import configparser
from pathlib import Path
from importlib import import_module
from pprint import pprint
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class QCAuto:
    folder_name = 'qc_app_folder'
    p_config = Path(f'{os.path.dirname(__file__)}/{folder_name}/')

    def __init__(self):
        pass

    def calc_call(self):
        list_machine = self._get_config_machine()
        for machine in list_machine:
            list_items = self._read_config(machine)
            for list_item in list_items:
                qc = QCAnalysis(list_item)
                qc.analysis()

    def _get_config_machine(self):
        self.config_ini = configparser.ConfigParser()
        list_machine = []
        for p in self.p_config.glob('setting*'):
            self.config_ini.read(p)
            list_machine.append(self.config_ini['DEFAULT']['machine_name'])
        return list_machine

    def _read_config(self, machine_name):
        self.config_ini = configparser.ConfigParser()
        config_ini_machine = configparser.ConfigParser()
        v_list_machine = {}

        # 装置取得
        for p in self.p_config.glob('setting*'):
            self.config_ini.read(p, 'UTF-8')
            c_machine_name = self.config_ini['DEFAULT']['machine_name']
            if machine_name == c_machine_name:
                config_ini_machine.read(p, 'UTF-8')
                break
        else:
            raise SystemError('setting*.iniがありません')

        # 辞書取得
        list_items = []
        for i in config_ini_machine.sections():
            v = {}
            for k, value in config_ini_machine[i].items():
                if value == 'True':
                    v[k] = True
                elif value == 'False':
                    v[k] = False
                else:
                    v[k] = value
            list_items.append(v)
        return list_items


# QCappでも使用するので、別のクラスにして解析。
class QCAnalysis:
    # 一時ファイルの名称。基本変えないのでクラス変数にしとく。
    list_meas_tmp = 'list_meas_tmp.pkl'

    def __init__(self, list_item):
        self.list_item = list_item

    def analysis(self, is_getdata = True):
        list_item = self.list_item
        # フォルダのオブジェクト化
        p = Path(list_item['stem_data'] + list_item['data_folder_name'])

        p_mid = Path(list_item['stem_mid'] + list_item['folder_name'])
        p_mid_str = Path(list_item['stem_mid'] + list_item['mid_str'])
        p_csv = Path(list_item['stem_csv'] + list_item['csv_name'])
        p_save = Path(list_item['stem_excel'] + list_item['folder_name'])
        p_trend = Path(list_item['stem_excel'] + list_item['excel_trend'])
        search_plate = list_item['search_plate']
        search_word = list_item['search_word']

        p_list_meas_tmp = Path(list_item['stem_mid'] + list_item['folder_name'] + '/' + self.list_meas_tmp)

        # ファイル回収のためのpathlib化。
        if is_getdata:
            p_from = Path(list_item['data_folder'])
        else:
            p_from = ''

        # インスタンス化して処理
        module = import_module(list_item['module_name'])
        cls = getattr(module, list_item['class_name'])

        # search_wordを変えないものはFalseに変更
        if search_word == '':
            search_word = False

        # is_data_getの場合はファイルコピーも実施。
        # IPRO8 SPCの場合はbaselineが必要なので、別でインスタンス化
        if list_item['item_name'] == 'spc':
            p_baseline = Path(list_item['stem_data'] + list_item['data_baseline_name'])
            if list_item['is_data_get']:
                if list_item['is_p_mid_str']:
                    t = cls(p, p_mid, p_from, p_mid_str, p_baseline=p_baseline, search_plate=search_plate,
                            search_word=search_word)
                else:
                    t = cls(p, p_mid, p_from, p_baseline=p_baseline, search_plate=search_plate, search_word=search_word)
            else:
                if list_item['is_p_mid_str']:
                    t = cls(p, p_mid, p_from='', p_mid_str=p_mid_str, p_baseline=p_baseline, search_plate=search_plate,
                            search_word=search_word)
                else:
                    t = cls(p, p_mid, p_baseline=p_baseline, search_plate=search_plate, search_word=search_word)
        # その他
        else:
            if list_item['is_data_get']:
                if list_item['is_p_mid_str']:
                    t = cls(p, p_mid, p_from, p_mid_str, search_plate=search_plate, search_word=search_word)
                else:
                    t = cls(p, p_mid, p_from, search_plate=search_plate, search_word=search_word)
            else:
                if list_item['is_p_mid_str']:
                    t = cls(p, p_mid, p_from='', p_mid_str=p_mid_str, search_plate=search_plate,
                            search_word=search_word)
                else:
                    t = cls(p, p_mid, search_plate=search_plate, search_word=search_word)

        # ファイルデータ取得の切り分け。取得しない場合は一時ファイルを返す。
        if is_getdata:
            p_from = Path(list_item['data_folder'])
        else:
            # ファイルがない時はNoneを返す。
            if not (p_list_meas_tmp.exists()):
                return None
            with open(p_list_meas_tmp, 'rb') as f:
                list_meas = pickle.load(f)
            self.t = t
            return list_meas

        self.t = t
        if is_getdata:
            t.save_result_csv(p_csv)
            t.save_excels(p_save)
            t.save_excel_trend(p_trend)
        else:
            self.list_ignore = t.list_ignore
            return t.list_meas

    def read_ignore_list(self):
        return self.t.list_ignore

    def write_ignore_list(self, list_ignore):
        self.t.write_ignore_list(list_ignore)

    def read_ref_list(self):
        return self.t.list_ref

    def write_ref_list(self, list_ignore):
        self.t.write_ref_list(list_ignore)


if __name__ == '__main__':
    # qc_appと合わせるため、カレントディレクトリを1階層上げる。
    os.chdir('../')
    q = QCAuto()
    q.calc_call()


