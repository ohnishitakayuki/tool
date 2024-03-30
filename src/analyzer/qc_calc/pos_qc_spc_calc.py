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
from pos_qc.pos_qc_spc import PosQcSpc


class PosQcSpcCalc(PosQcCalc):
    short_time = 20     # 2回測定の測定時間差の最大値。単位min。
    date_cut_off = datetime(2023, 11, 10, 0, 0, 0)  # この日時より前のものは計算しない。
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/posQC_trend/SPC Trend format.xlsx')
    excel_file_stem = 'SPC'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '*.lms'
    search_meas_file = '**/*.lms'

    def __init__(self, p, p_mid=None, p_from=None, p_baseline=None, is_reload=False,
                 search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload)
        self.p_baseline = p_baseline

        # baselineの日付、アドレスリストを作成。
        list_p_baseline = []
        for p_baseline_tmp in p_baseline.glob('????????'):
            meas_time_baseline = datetime.strptime(p_baseline_tmp.name, '%Y%m%d')
            list_tmp = [meas_time_baseline, p_baseline_tmp]
            list_p_baseline.append(list_tmp )
        self.list_p_baseline = list_p_baseline

        # あとで消す。
        # self.list_p_baseline = list(p_baseline.glob(self.search_meas_file))

    def _get_meas_combination(self, list_meas_row):
        # SPCの組み合わせを探す関数。
        # 3連続測定を探す
        list_meas = []

        for i in range(len(list_meas_row) - 2):
            if list_meas_row[i][0] < self.date_cut_off:  # 設定よりも前のデータは読まない
                continue
            is_analysis = False
            meas_time_diff1 = (list_meas_row[i + 1][0] - list_meas_row[i][0]).total_seconds()
            meas_time_diff2 = (list_meas_row[i + 2][0] - list_meas_row[i + 1][0]).total_seconds()
            s_time = self.short_time * 60
            if meas_time_diff1 < s_time and meas_time_diff2 < s_time:
                # 2個手前でないものの処理。次の次の処理がshort timeより短いものはカットしている。
                if i + 3 < len(list_meas_row):
                    meas_next_time_diff = list_meas_row[i + 3][0] - list_meas_row[i + 2][0]
                    if meas_next_time_diff.total_seconds() > self.short_time * 60:
                        is_analysis = True
                # 2個手前は無条件で解析
                else:
                    is_analysis = True
            if is_analysis:
                list_meas_tmp = [list_meas_row[i + 1][0], list_meas_row[i][1], list_meas_row[i+1][1],
                                list_meas_row[i+2][1]]
                list_meas.append(list_meas_tmp)
        return list_meas

    def _read_pickle(self, list_meas_set):
        # SPCを読み込む
        list_p = [list_meas_set[1], list_meas_set[2], list_meas_set[3]]

        # ここでBaselineを選択
        # 日付形式にしたいところ
        list_p_baseline_select = []
        for list_baseline in self.list_p_baseline:
            if list_meas_set[0] > list_baseline[0]:
                list_p_baseline_select = list_baseline
            else:
                break
        if list_p_baseline_select == []:
            raise FileNotFoundError('適応するbaselineファイルがありません。')

        list_p_b = list(list_p_baseline_select[1].glob(self.search_meas_file))
        c = PosQcSpc(list_p_b, list_p)
        return c

    def save_result_csv(self, p_csv=False):
        # Global Shortのテーブルを作成して、csvとして保存
        # そんなに数は多くないので、カテゴリーごとにソースを作ろう。
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            list_result_tmp = [r.meas_start, r.x_spc_rot_max, r.y_spc_rot_max, r.x_spc_1st_max, r.y_spc_1st_max]
            list_result.append(list_result_tmp)
        # 自分でカラム名つけてね。
        df = pd.DataFrame(list_result, columns=['Date', 'spc_rot_x', 'spc_rot_y', 'spc_1st_x', 'spc_1st_y'])
        if p_csv:
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
                            r.x_spc_nocorr_max,
                            r.y_spc_nocorr_max,
                            r.x_spc_rot_max,
                            r.y_spc_rot_max,
                            r.x_spc_1st_max,
                            r.y_spc_1st_max,
                            r.x_spc_data1_nocorr,
                            r.y_spc_data1_nocorr,
                            r.x_spc_data1_rot,
                            r.y_spc_data1_rot,
                            r.x_spc_data1_1st,
                            r.y_spc_data1_1st,
                            r.x_spc_data2_nocorr,
                            r.y_spc_data2_nocorr,
                            r.x_spc_data2_rot,
                            r.y_spc_data2_rot,
                            r.x_spc_data2_1st,
                            r.y_spc_data2_1st,
                            r.x_spc_data3_nocorr,
                            r.y_spc_data3_nocorr,
                            r.x_spc_data3_rot,
                            r.y_spc_data3_rot,
                            r.x_spc_data3_1st,
                            r.y_spc_data3_1st,
                        ]
        return list_result_tmp


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/IPRO8/global_str/')
    # p_from = Path('//172.26.31.68/d/measurement/result/QC/Global')
    p_baseline = Path(os.path.dirname(__file__) + '/../../../data/IPRO8/baseline/')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/IPRO8/spc/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/spc/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/SPC Trend.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/excel_trend/SPC Trend.xlsx')
    t = PosQcSpcCalc(p, p_mid, p_baseline = p_baseline)
    t.get_result_list()
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


    # ignoreリストを作る時に使用
    # list_ignore = t.list_meas[:1]
    # t.write_ignore_list(list_ignore)
    # print(t.save_result_csv())

