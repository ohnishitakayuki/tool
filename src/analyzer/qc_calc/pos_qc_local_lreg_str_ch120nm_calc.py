import os
import sys
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime
import openpyxl
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pos_qc_calc import PosQcCalc
from pos_qc.pos_qc_lreg import PosQcLreg
from pos_qc_local_lreg_str_ch240nm_calc import PosQcLocalLregStrCH240nmCalc


class PosQcLocalLregStrCH120nmCalc(PosQcLocalLregStrCH240nmCalc):
    short_time = 50     # 2回測定の測定時間差の最大値。単位min。
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/posQC_trend/Local Lreg STR CH120nm Trend format.xlsx')
    excel_file_stem = 'Local_Lreg_STR_120nm'

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload)

    def _read_pickle(self, list_meas_set):
        # Local Shortの関数を読み込む
        # さらにexcel formatファイルの場所を書き換えている。
        c = PosQcLreg(list_meas_set[1], list_meas_set[2])
        c.p_excel = Path(os.path.dirname(__file__) + '/../../excel_template/posQC/Local Lreg STR CH120nm format.xlsx')
        return c

    def save_result_csv(self, p_csv=False):
        # Local Shortのテーブルを作成して、csvとして保存
        # そんなに数は多くないので、カテゴリーごとにソースを作ろう。
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            list_result_tmp = [r.meas_start_1st, r.x_3s_1st, r.y_3s_1st]
            list_result.append(list_result_tmp)
        # 自分でカラム名つけてね。
        df = pd.DataFrame(list_result, columns=['Date', 'local_str_ch120nm_x', 'local_str_ch120nm_y'])
        if p_csv:
            df.to_csv(p_csv)
        else:
            return df

if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/IPRO8/local_lreg_str_ch120nm/')
    p_from = Path('//172.26.31.68/d/measurement/result/QC/Local_CH120')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/IPRO8/local_lreg_str_ch120nm/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/local_lreg_str_ch120nm/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/Local Lreg STR CH120nm Trend.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/excel_trend/Local Lreg STR CH120nm Trend.xlsx')
    t = PosQcLocalLregStrCH120nmCalc(p, p_mid, p_from,)
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


    # ignoreリストを作る時に使用
    # list_ignore = t.list_meas[:1]
    # t.write_ignore_list(list_ignore)
    # print(t.save_result_csv())

