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
from cd_qc.cd_qc_nft_dynamic import CdQcNftDynamic


class CdQcNftDynamicCalc(CdQcCalc):
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/cdQC_trend/NFT Dynamic Trend.xlsx')
    excel_file_stem = 'NFT_Dynamic'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '*.csv'
    search_meas_file = '**/*.csv'

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload, search_plate, search_word)

    def _read_pickle(self, list_meas_set):
        # Nft Dynamicを読み込む
        c = CdQcNftDynamic(list_meas_set[1], list_meas_set[2])
        return c

    def save_result_csv(self, p_csv=False):
        # Global Shortのテーブルを作成して、csvとして保存
        # そんなに数は多くないので、カテゴリーごとにソースを作ろう。
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            list_result_tmp = [r.meas_start, r.rep_3s_hor_space, r.rep_3s_ver_space,
                               r.slope_1st_line_hor_space, r.slope_1st_line_ver_space]
            list_result.append(list_result_tmp)
        # 自分でカラム名つけてね。
        df = pd.DataFrame(list_result, columns=['Date', 'nft_dynamic_hor', 'nft_dynamic_ver',
                                                'nft_dynamic_slope_hor', 'nft_dynamic_slope_ver'
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
        list_result_tmp = [
                            r.meas_start,
                            r.plate_type,
                            r.meas_time,
                            f'{r.column_num}-{r.row_num}',
                            r.rep_3s_hor_space,
                            r.rep_3s_ver_space,
                            r.slope_1st_line_hor_space,
                            r.slope_1st_line_ver_space,
                            r.slope_2nd_line_hor_space,
                            r.slope_2nd_line_ver_space,
                            r.diff_mean_hor_space,
                            r.diff_mean_ver_space,
                            r.cd_mean_1st_hor_space,
                            r.cd_mean_2nd_hor_space,
                            r.cd_mean_1st_ver_space,
                            r.cd_mean_2nd_ver_space,
                            r.cd_3s_1st_hor_space,
                            r.cd_3s_2nd_hor_space,
                            r.cd_3s_1st_ver_space,
                            r.cd_3s_2nd_ver_space,
                            r.cd_max_1st_hor_space,
                            r.cd_max_2nd_hor_space,
                            r.cd_max_1st_ver_space,
                            r.cd_max_2nd_ver_space,
                            r.cd_min_1st_hor_space,
                            r.cd_min_2nd_hor_space,
                            r.cd_min_1st_ver_space,
                            r.cd_min_2nd_ver_space,
                            r.cd_range_1st_hor_space,
                            r.cd_range_2nd_hor_space,
                            r.cd_range_1st_ver_space,
                            r.cd_range_2nd_ver_space,
                            r.rep_3s_hor_pitch,
                            r.rep_3s_ver_pitch,
                            r.diff_mean_hor_pitch,
                            r.diff_mean_ver_pitch,
                            r.cd_mean_1st_hor_pitch,
                            r.cd_mean_2nd_hor_pitch,
                            r.cd_mean_1st_ver_pitch,
                            r.cd_mean_2nd_ver_pitch,
                            r.cd_3s_1st_hor_pitch,
                            r.cd_3s_2nd_hor_pitch,
                            r.cd_3s_1st_ver_pitch,
                            r.cd_3s_2nd_ver_pitch,
                            r.cd_max_1st_hor_pitch,
                            r.cd_max_2nd_hor_pitch,
                            r.cd_max_1st_ver_pitch,
                            r.cd_max_2nd_ver_pitch,
                            r.cd_min_1st_hor_pitch,
                            r.cd_min_2nd_hor_pitch,
                            r.cd_min_1st_ver_pitch,
                            r.cd_min_2nd_ver_pitch,
                            r.cd_range_1st_hor_pitch,
                            r.cd_range_2nd_hor_pitch,
                            r.cd_range_1st_ver_pitch,
                            r.cd_range_2nd_ver_pitch,
                            r.afqv_1st_hor,
                            r.afqv_2nd_hor,
                            r.afqv_1st_ver,
                            r.afqv_2nd_ver,
                            r.white_band_1st_hor,
                            r.white_band_2nd_hor,
                            r.white_band_1st_ver,
                            r.white_band_2nd_ver,
                        ]
        return list_result_tmp


#  oldはExcelの貼り付けを変えるためにオーバーライド
class CdQcNftDynamicOldCalc(CdQcNftDynamicCalc):
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/cdQC_trend/NFT Dynamic old Trend.xlsx')
    excel_file_stem = 'NFT_Dynamic_old'
    excel_start_row = 1128
    excel_start_column = 1

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload, search_plate, search_word)


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/E3640/nft_dynamic/')
    p_from = Path('//172.26.31.68/d/measurement/result/QC/Screen_Linearity')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/E3640/nft_dynamic/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/E3640/nft_dynamic/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/E3640/Nft Dynamic.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/E3640/excel_trend/nft dynamic.xlsx')
    t = CdQcNftDynamicCalc(p, p_mid, search_plate=True)
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


    # ignoreリストを作る時に使用
    # list_ignore = t.list_meas[:1]
    # t.write_ignore_list(list_ignore)
    # print(t.save_result_csv())
