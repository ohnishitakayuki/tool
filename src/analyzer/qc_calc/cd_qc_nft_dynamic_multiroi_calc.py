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
from cd_qc.cd_qc_nft_dynamic_multiroi import CdNftDynamicMultiRoi


class CdQcNftDynamicMultiRoiCalc(CdQcCalc):
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/cdQC_trend/NFT dynamic multiROI.xlsx')
    excel_file_stem = 'NFT_Dynamic_multiROI'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '*.csv'
    search_meas_file = '**/*.csv'
    search_normal_file = '_multiROI_Normal_'
    search_no_overlap_file = '_multiROI_No_overlap_'
    search_time = 60  # 0度と270度の時間差限界。単位分。

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload, search_plate, search_word)

    def _get_meas_combination(self, list_meas_row):
        # XY scanを探す関数。
        list_meas = []
        is_search_normal = True
        for list_meas_f in list_meas_row:
            print(list_meas_f)
            p = Path(list_meas_f[1])
            file_name = p.name

            if is_search_normal:
                # 0degの時
                # print(file_name)
                if self.search_normal_file in file_name:
                    list_meas_tmp = list_meas_f
                    meas_date_normal = list_meas_f[0]
                    is_search_normal = False
            else:
                if self.search_no_overlap_file in file_name:

                    meas_date_no_overlap = list_meas_f[0]
                    meas_diff = meas_date_no_overlap - meas_date_normal
                    if meas_diff.seconds < self.search_time * 60:
                        # normalとno overlapの差がsearch_timeより小さいときに追加
                        list_meas_tmp.append(list_meas_f[1])
                        list_meas.append(list_meas_tmp)
                    is_search_normal = True

        return list_meas

    def _read_pickle(self, list_meas_set):
        # QcNftDynamicMultiroiを読み込む
        c = CdNftDynamicMultiRoi(list_meas_set[1], list_meas_set[3], list_meas_set[2])
        return c

    def save_result_csv(self, p_csv=False):
        # Global Shortのテーブルを作成して、csvとして保存
        # そんなに数は多くないので、カテゴリーごとにソースを作ろう。
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            list_result_tmp = [r.meas_start, r.rep_3s_hor, r.rep_3s_ver]
            list_result.append(list_result_tmp)
        # 自分でカラム名つけてね。
        df = pd.DataFrame(list_result, columns=['Date', 'nft_dynamic_hor', 'nft_dynamic_ver',])
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
                            f'{r.column_num}-{r.row_num}',
                            r.rep_3s_hor,
                            r.rep_3s_ver,
                            r.cd_diff_hor,
                            r.cd_diff_ver,
                            r.cd_mean_ref_hor,
                            r.cd_mean_hor,
                            r.cd_mean_ref_ver,
                            r.cd_mean_ver,
                            r.cd_3s_ref_hor,
                            r.cd_3s_hor,
                            r.cd_3s_ref_ver,
                            r.cd_3s_ver,
                            r.cd_max_ref_hor,
                            r.cd_max_hor,
                            r.cd_max_ref_ver,
                            r.cd_max_ver,
                            r.cd_min_ref_hor,
                            r.cd_min_hor,
                            r.cd_min_ref_ver,
                            r.cd_min_ver,
                            r.cd_range_ref_hor,
                            r.cd_range_hor,
                            r.cd_range_ref_ver,
                            r.cd_range_ver,
                        ]
        return list_result_tmp


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../test/test_data/data_cd_qc_nft_dynamic_multiroi/')
    # p_from = Path('//172.26.31.68/')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/E3650/nft_dynamic_multiroi/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/E3650/nft_dymamic_multiroi/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/E3650/nft_dymamic_multiroi.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/E3650/nft_dymamic_multiroi.xlsx')
    t = CdQcNftDynamicMultiRoiCalc(p, p_mid, search_plate=True)
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


