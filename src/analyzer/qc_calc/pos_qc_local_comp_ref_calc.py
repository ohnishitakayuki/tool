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
from pos_qc.pos_qc_lpos import PosQcLpos


class PosQcLocalCompRefCalc(PosQcCalc):
    short_time = 40     # 2回測定の測定時間差の最大値。単位min。
    p_mid = '../../../mid_data/pos_qc_lpos_calc/'
    ignore_list_name = 'ignore_list.pkl'
    reference_list_name = 'reference_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/posQC_trend/Local Comp Ref Trend format.xlsx')
    excel_file_stem = 'Local_Comp_Ref'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '*.lms'
    search_meas_file = '**/*.lms'
    search_normal = '_Local_V'
    search_sl = '_Local_SL_V'

    def __init__(self, p, p_mid=None, p_from=None, p_mid_str=None, is_reload=False, search_plate=False,
                 search_word=False):
        if p_mid_str:
            self.p_mid_str = p_mid_str
        super().__init__(p, p_mid, p_from, is_reload)

    def _get_meas_combination(self, list_meas_row):
        # Local Longの組み合わせを探す関数。
        # SL→Meas→SL→Meas→SLのものを探してから1個目だけをリストアップ
        # print(self.list_ref)
        list_meas_str = []
        j = 0
        for i in range(len(list_meas_row) - 4):
            if not(self.search_sl in list_meas_row[i][1]):
                continue
            meas_time_diff1 = list_meas_row[i + 1][0] - list_meas_row[i][0]
            if not(self.search_normal in list_meas_row[i+1][1] and meas_time_diff1.total_seconds() < self.short_time * 60):
                continue
            meas_time_diff2 = list_meas_row[i + 2][0] - list_meas_row[i][0]
            if not (self.search_sl in list_meas_row[i + 2][1] and meas_time_diff2.total_seconds() < self.short_time * 60):
                continue
            meas_time_diff3 = list_meas_row[i + 3][0] - list_meas_row[i][0]
            if not (self.search_normal in list_meas_row[i + 3][1] and meas_time_diff3.total_seconds() < self.short_time * 60):
                continue
            meas_time_diff4 = list_meas_row[i + 4][0] - list_meas_row[i][0]
            if not (self.search_sl in list_meas_row[i + 4][1] and meas_time_diff4.total_seconds() < self.short_time * 60):
                continue

            # Shortで一度解析しているか確認。解析していないものは壊れファイルということでスキップ。
            p_test = Path(self.p_mid_str / f"{list_meas_row[i][0].strftime('%Y%m%d_%H%M%S')}.pkl")
            if not(p_test.exists()):
                continue

            list_meas_tmp = [list_meas_row[i][0], list_meas_row[i][1], list_meas_row[i+1][1],
                             list_meas_row[i+2][1], list_meas_row[i+3][1], list_meas_row[i+4][1]]
            list_meas_str.append(list_meas_tmp)

        # 初回セット。リファレンス(後半3つ)はここでは初期値として、_adapt_refで当てはめる。そうしないとignoreリスト取得などに対応できない。
        list_meas = []
        for i in range(len(list_meas_str)):
            list_tmp = [list_meas_str[i][0], list_meas_str[i][1], list_meas_str[i][2], list_meas_str[i][3],
                        list_meas_str[0][1], list_meas_str[0][2], list_meas_str[0][3]]
            list_meas.append(list_tmp)

        return list_meas

    def _read_pickle(self, list_meas_set):
        # Local Longの関数を読み込む
        # 1: SL0, 2: Meas1, 3: SL1, 4: Meas2, 5: SL2
        c = PosQcLpos(list_meas_set[2], list_meas_set[5],
                      list_meas_set[1], list_meas_set[3], list_meas_set[4], list_meas_set[6])
        return c

    # refの設定を行う。結構複雑なので注意。
    # 対象データは直前のrefを使用。
    # refになったものは解析しない。
    def _adapt_ref(self, list_meas):
        if self.list_ref != []:
            list_meas_new = []
            is_first = True
            for list_meas_data in list_meas:
                list_ref_tmp = []
                is_same_data = False
                # 各referenceを回す。
                # 初回は同じデータになるのでスキップ
                if is_first:
                    is_first = False
                    continue
                # refデータで回す。
                for list_ref_data in self.list_ref:
                    # refの方が小さい間は値を入れて飛ばす。
                    if list_meas_data[0] > list_ref_data[0]:
                        list_ref_tmp = list_ref_data
                    # 同じときはrefデータ扱いなので解析そのものスキップさせる。
                    elif list_meas_data[0] == list_ref_data[0]:
                        is_same_data = True
                        break
                    # refのほうが新しいのでスキップして解析へ。
                    else:
                        break
                # refデータにひっかからなかったやつはそのまま。
                if list_ref_tmp == []:
                    list_meas_tmp = list_meas_data
                # refデータをmeasに入れ込む。
                else:
                    list_meas_tmp = [list_meas_data[0], list_meas_data[1], list_meas_data[2], list_meas_data[3],
                                  list_ref_tmp[1], list_ref_tmp[2], list_ref_tmp[3]]
                # refデータ以外を新しいlist_measに入れる。
                if not is_same_data:
                    list_meas_new.append(list_meas_tmp)
            list_meas = list_meas_new

        # refになにも設定されていない場合、初めの値をrefとするため、初めの値を削除する。
        else:
            list_meas = list_meas[1:]
        return list_meas

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
        df = pd.DataFrame(list_result, columns=['Date', 'local_comp_ref_x', 'local_comp_ref_y'])
        if p_csv:
            df.to_csv(p_csv)
        else:
            return df

    def _qc_check_value(self, r):
        # トレンドに入れたくない場合はここで条件式を書く。Falseではじく
        is_data = True
        x_rep = r.x_3s_1st
        y_rep = r.y_3s_1st
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
                            r.x_3s_nocorr,
                            r.y_3s_nocorr,
                            r.x_3s_rot,
                            r.y_3s_rot,
                            r.x_3s_1st,
                            r.y_3s_1st,
                            r.a0_data1,
                            r.a1_data1,
                            r.a2_data1,
                            r.b0_data1,
                            r.b1_data1,
                            r.b2_data1,
                            r.rot_data1,
                            r.a0_data2,
                            r.a1_data2,
                            r.a2_data2,
                            r.b0_data2,
                            r.b1_data2,
                            r.b2_data2,
                            r.rot_data2,
                        ]
        return list_result_tmp


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/IPRO8/local_str/')
    p_from = Path('//172.26.31.68/d/measurement/result/QC/Local')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/IPRO8/local_comp_ref/')
    p_mid_str = Path(os.path.dirname(__file__) + '/../../../mid_data/IPRO8/local_str/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/local_comp_ref/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/Local Comp Ref Trend.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/IPRO8/excel_trend/Local Comp Ref Trend.xlsx')
    t = PosQcLocalCompRefCalc(p, p_mid, p_from, p_mid_str,)
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


    # ignoreリストを作る時に使用
    # list_ignore = t.list_meas[:1]
    # t.write_ignore_list(list_ignore)
    # print(t.save_result_csv())

