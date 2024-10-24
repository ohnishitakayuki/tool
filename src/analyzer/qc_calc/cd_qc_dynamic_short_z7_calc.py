import os
import sys
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime
import openpyxl

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from cd_qc_calc import CdQcCalc
from cd_qc.cd_qc_dynamic_short_z7 import CdQcDynamicShortZ7


class CdQcDynamicShortZ7Calc(CdQcCalc):
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/cdQC_trend/Dynamic Short Z7 Trend.xlsx')
    excel_file_stem = 'Dynamic Short'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '**/DAT-Dynamic_Short*/*/ResultMain.CSV'
    search_meas_file = '**/DAT-Dynamic_Short*/*/ResultMain.CSV'

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload, search_plate, search_word)

    def _read_pickle(self, list_meas_set):
        # Dynamic Shortを読み込む
        c = CdQcDynamicShortZ7(list_meas_set[1], list_meas_set[2])
        return c

    def save_result_csv(self, p_csv=False):
        # Global Shortのテーブルを作成して、csvとして保存
        # そんなに数は多くないので、カテゴリーごとにソースを作ろう。
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            list_result_tmp = [r.meas_start, r.rep_3s_1st,]
            list_result.append(list_result_tmp)
        # 自分でカラム名つけてね。
        df = pd.DataFrame(list_result, columns=['Date', 'dynamic_short',
                                                ])
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
        print(r.meas_start)
        list_result_tmp = [
                            r.meas_start,
                            r.plate_type,
                            r.meas_time,
                            f'{r.column_num}-{r.row_num}',
                            r.rep_3s_raw,
                            r.rep_3s_1st,
                            r.slope_average,
                            r.rep_3s_raw_chip1,
                            r.rep_3s_raw_chip2,
                            r.rep_3s_raw_chip3,
                            r.rep_3s_1st_chip1,
                            r.rep_3s_1st_chip2,
                            r.rep_3s_1st_chip3,
                            r.rep_3s_raw_110nm,
                            r.rep_3s_raw_200nm,
                            r.rep_3s_raw_400nm,
                            r.rep_3s_raw_750nm,
                            r.rep_3s_1st_110nm,
                            r.rep_3s_1st_200nm,
                            r.rep_3s_1st_400nm,
                            r.rep_3s_1st_750nm,
                            r.rep_3s_raw_iso_line,
                            r.rep_3s_raw_iso_space,
                            r.rep_3s_raw_ls_line,
                            r.rep_3s_raw_ls_space,
                            r.rep_3s_1st_iso_line,
                            r.rep_3s_1st_iso_space,
                            r.rep_3s_1st_ls_line,
                            r.rep_3s_1st_ls_space,
                            r.rep_3s_raw_x,
                            r.rep_3s_raw_y,
                            r.rep_3s_1st_x,
                            r.rep_3s_1st_y,
                        ]
        return list_result_tmp


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/Z7/dynamic_short')
    p_from = Path('//172.26.33.50/d/ZSData/QC')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/Z7/dynamic_short/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/Z7/dynamic_short/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/Z7/Dynamic Short Z7.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/Z7/excel_trend/dynamic_short z7.xlsx')
    t = CdQcDynamicShortZ7Calc(p, p_mid, p_from, search_plate=True)
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


    # ignoreリストを作る時に使用
    # list_ignore = t.list_meas[:1]
    # t.write_ignore_list(list_ignore)
    # print(t.save_result_csv())

