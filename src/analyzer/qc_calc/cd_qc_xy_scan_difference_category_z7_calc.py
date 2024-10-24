import os
import sys
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime
from pprint import pprint
import openpyxl

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from cd_qc_calc import CdQcCalc
from cd_qc.cd_qc_xy_scan_difference_category_z7 import CdQcXyScanDifferenceCategoryZ7


class CdQcXyScanDifferenceCategoryZ7Calc(CdQcCalc):
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/cdQC_trend/XY scan difference category Z7 Trend.xlsx')
    excel_file_stem = 'XY scan difference category'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '**/DAT-XY_scan_difference_category_*/*/ResultMain.CSV'
    search_meas_file = '**/*.csv'
    search_0deg_file = '_R0_'
    search_270deg_file = '_R90_'
    search_time = 120  # 0度と270度の時間差限界。単位分。

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload, search_plate, search_word)

    def _get_meas_combination(self, list_meas_row):
        # XY scanを探す関数。
        list_meas = []
        is_search_rot0 = True
        for list_meas_f in list_meas_row:
            p = Path(list_meas_f[1])
            file_name = str(p)

            if is_search_rot0:
                # 0degの時
                if self.search_0deg_file in file_name:
                    list_meas_tmp = list_meas_f
                    meas_date_rot0 = list_meas_f[0]
                    is_search_rot0 = False
            else:
                if self.search_270deg_file in file_name:

                    meas_date_rot270 = list_meas_f[0]
                    meas_diff = meas_date_rot270 - meas_date_rot0
                    if meas_diff.seconds < self.search_time * 60:
                        # 0度と270度の差がsearch_timeより小さいときに追加
                        list_meas_tmp.append(list_meas_f[1])
                        list_meas.append(list_meas_tmp)
                    is_search_rot0 = True

        return list_meas

    def _read_pickle(self, list_meas_set):
        # XY scan differenceを読み込む
        print(list_meas_set)
        c = CdQcXyScanDifferenceCategoryZ7(list_meas_set[1], list_meas_set[3], list_meas_set[2])
        return c

    def save_result_csv(self, p_csv=False):
        # Global Shortのテーブルを作成して、csvとして保存
        # そんなに数は多くないので、カテゴリーごとにソースを作ろう。
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            list_result_tmp = [r.meas_start, r.xy_space]
            list_result.append(list_result_tmp)
        # 自分でカラム名つけてね。
        df = pd.DataFrame(list_result, columns=['Date', 'xy_scan_difference_category'])
        if p_csv:
            p_csv.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(p_csv)
        else:
            return df

    def _qc_check_value(self, r):
        # トレンドに入れたくない場合はここで条件式を書く。Falseではじく
        is_data = True
        return is_data

    def _get_list_result_tmp(self, r):
        # Excel Trendに乗せる値を抽出
        list_result_tmp = [
                            r.meas_start,
                            r.plate_type,
                            r.meas_time,
                            r.meas_time_0deg,
                            r.meas_time_90deg,
                            r.xy_space,
                            r.xy_line,
                            r.xy_pitch,
                        ]
        return list_result_tmp


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/Z7/xy_scan_difference_category')
    p_from = Path('//172.26.33.50/d/ZSData/QC')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/Z7/xy_scan_difference_category/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/Z7/xy_scan_difference_category/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/Z7/XY scan difference category Z7.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/Z7/excel_trend/xy_scan_difference_category z7.xlsx')
    t = CdQcXyScanDifferenceCategoryZ7Calc(p, p_mid, p_from, search_plate=False)
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


