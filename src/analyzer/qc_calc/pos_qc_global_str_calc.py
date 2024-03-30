import os
import sys
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime
import openpyxl

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pos_qc_calc import PosQcCalc
from pos_qc.pos_qc_gpos import PosQcGpos


class PosQcGlobalStrCalc(PosQcCalc):
    short_time = 20     # 2回測定の測定時間差の最大値。単位min。
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/posQC_trend/Global STR Trend format.xlsx')
    excel_file_stem = 'Global_STR'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '*.lms'
    search_meas_file = '**/*.lms'

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload)


    def _get_meas_combination(self, list_meas_row):
        # Global Shortの組み合わせを探す関数。
        list_meas = []
        for i in range(len(list_meas_row) - 1):
            is_analysis = False
            meas_time_diff = list_meas_row[i + 1][0] - list_meas_row[i][0]
            if meas_time_diff.total_seconds() < self.short_time * 60:
                # 2個手前でないものの処理。次の次の処理がshort timeより短いものはカットしている。
                if i + 2 < len(list_meas_row):
                    meas_next_time_diff = list_meas_row[i + 2][0] - list_meas_row[i + 1][0]
                    if meas_next_time_diff.total_seconds() > self.short_time * 60:
                        is_analysis = True
                # 2個手前は無条件で解析
                else:
                    is_analysis = True
            if is_analysis:
                list_meas_tmp = [list_meas_row[i + 1][0], list_meas_row[i + 1][1], list_meas_row[i][1]]
                list_meas.append(list_meas_tmp)
        return list_meas

    def _read_pickle(self, list_meas_set):
        # Global Shortの関数を読み込む
        # リストの0番目が時刻、1が1つめ、2が2つめのパス。
        c = PosQcGpos(list_meas_set[1], list_meas_set[2])
        return c

    def save_result_csv(self, p_csv=False):
        # Global Shortのテーブルを作成して、csvとして保存
        # そんなに数は多くないので、カテゴリーごとにソースを作ろう。
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            list_result_tmp = [r.meas_start_1st, r.x_3s_s1_rot, r.y_3s_s1_rot]
            list_result.append(list_result_tmp)
        # 自分でカラム名つけてね。
        df = pd.DataFrame(list_result, columns=['Date', 'global_str_x', 'global_str_y'])
        if p_csv:
            df.to_csv(p_csv)
        else:
            return df

    def _qc_check_value(self, r):
        # トレンドに入れたくない場合はここで条件式を書く。Falseではじく
        is_data = True
        x_rep = r.x_3s_s1_1st
        y_rep = r.y_3s_s1_1st
        if x_rep > 1 or y_rep > 1:
            is_data = False
        return is_data

    def _get_meas_time(self, r):
        # Excelファイル名用。1stあり。
        meas_time = r.meas_start_1st.strftime('%Y%m%d_%H%M%S')
        return meas_time

    def _get_list_result_tmp(self, r):
        # Excel Trendに乗せる値を抽出
        list_result_tmp = [
                            r.meas_start_1st,
                            r.meas_time_1st,
                            r.meas_time_2nd,
                            r.x_3s_s1_nocorr,
                            r.y_3s_s1_nocorr,
                            r.x_3s_s1_rot,
                            r.y_3s_s1_rot,
                            r.x_3s_s1_1st,
                            r.y_3s_s1_1st,
                            r.a0_data1_s1,
                            r.a1_data1_s1,
                            r.a2_data1_s1,
                            r.b0_data1_s1,
                            r.b1_data1_s1,
                            r.b2_data1_s1,
                            r.rot_data1_s1,
                            r.a0_data2_s1,
                            r.a1_data2_s1,
                            r.a2_data2_s1,
                            r.b0_data2_s1,
                            r.b1_data2_s1,
                            r.b2_data2_s1,
                            r.rot_data2_s1,
                            r.x_3s_s2_nocorr,
                            r.y_3s_s2_nocorr,
                            r.x_3s_s2_rot,
                            r.y_3s_s2_rot,
                            r.x_3s_s2_1st,
                            r.y_3s_s2_1st,
                            r.a0_data1_s2,
                            r.a1_data1_s2,
                            r.a2_data1_s2,
                            r.b0_data1_s2,
                            r.b1_data1_s2,
                            r.b2_data1_s2,
                            r.rot_data1_s2,
                            r.a0_data2_s2,
                            r.a1_data2_s2,
                            r.a2_data2_s2,
                            r.b0_data2_s2,
                            r.b1_data2_s2,
                            r.b2_data2_s2,
                            r.rot_data2_s2,
                        ]
        return list_result_tmp


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/IPRO8/global_str/')
    p_from = Path('//172.26.31.68/d/measurement/result/QC/Global')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/IPRO8/global_str/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/global_str/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/Global STR Trend.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/excel_trend/Global STR Trend.xlsx')
    t = PosQcGlobalStrCalc(p, p_mid, p_from,)
    t.get_result_list()
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


    # ignoreリストを作る時に使用
    # list_ignore = t.list_meas[:1]
    # t.write_ignore_list(list_ignore)
    # print(t.save_result_csv())

