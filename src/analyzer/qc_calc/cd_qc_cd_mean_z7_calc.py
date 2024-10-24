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
from cd_qc.cd_qc_cd_mean_z7 import CdQcCdMeanZ7


class CdQcCdMeanZ7Calc(CdQcCalc):
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/cdQC_trend/CD mean Z7 Trend.xlsx')
    excel_file_stem = 'CD_mean'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '**/DAT-CD_mean*/*/ResultMain.CSV'
    search_meas_file = '**/DAT-CD_mean_*/*/ResultMain.CSV'
    search_ref_file = 'DAT-CD_mean_all'

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload, search_plate, search_word)

    def _get_meas_combination(self, list_meas_row):
        # CD refを探す関数。
        # 同一フォルダの'search_ref_file'が含まれているものをrefにする。
        # 2個以上あるときは一番新しいものを使用する。
        list_meas = []

        for list_meas_f in list_meas_row:
            p = Path(list_meas_f[1])

            # refファイルの場合はスキップ
            if self.search_ref_file in str(p):
                continue

            # 最新のrefファイルを取得。
            m_date = None
            p_ref = None

            # refファイルを探すためのループ
            for list_meas_fr in list_meas_row:
                p_ref_tmp = Path(list_meas_fr[1])

                # refファイル以外の場合はスキップ
                if not(self.search_ref_file in str(p_ref_tmp)):
                    continue
                print(list_meas_fr)
                m_date_tmp = datetime.fromtimestamp(p_ref_tmp.stat().st_mtime)
                if m_date is None:
                    m_date = m_date_tmp
                    p_ref = p_ref_tmp
                elif m_date_tmp > m_date:
                    m_date = m_date_tmp
                    p_ref = p_ref_tmp

            # refファイルが無いときはスキップ
            if p_ref == None:
                continue

            # refファイルをリストに追加
            list_meas_tmp = list_meas_f + [str(p_ref)]
            list_meas.append(list_meas_tmp)
        print(list_meas)
        return list_meas

    def _read_pickle(self, list_meas_set):
        # Nft Dynamicを読み込む
        c = CdQcCdMeanZ7(list_meas_set[1], list_meas_set[3], list_meas_set[2])
        return c

    def save_result_csv(self, p_csv=False):
        # Global Shortのテーブルを作成して、csvとして保存
        # そんなに数は多くないので、カテゴリーごとにソースを作ろう。
        list_instance = self._collect_result()
        list_result = []
        for r in list_instance:
            # 結果インスタンスから引き出す数値
            print(r.meas_start)
            try:
                list_result_tmp = [r.meas_start, r.hor_500nm_space, r.ver_500nm_space,
                                   r.hor_500nm_pitch, r.ver_500nm_pitch]
            except AttributeError:
                print('column is not found.')
                continue
            list_result.append(list_result_tmp)
        # 自分でカラム名つけてね。
        df = pd.DataFrame(list_result, columns=['Date', 'cd_mean_space_hor', 'cd_mean_space_ver',
                                                'cd_mean_pitch_hor', 'cd_mean_pitch_ver'
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
                            r.hor_100nm_space,
                            r.hor_200nm_space,
                            r.hor_500nm_space,
                            r.ver_100nm_space,
                            r.ver_200nm_space,
                            r.ver_500nm_space,
                            r.hor_100nm_pitch,
                            r.hor_200nm_pitch,
                            r.hor_500nm_pitch,
                            r.ver_100nm_pitch,
                            r.ver_200nm_pitch,
                            r.ver_500nm_pitch,
                        ]
        return list_result_tmp


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/Z7/cd_mean')
    p_from = Path('//172.26.33.50/d/ZSData/QC')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/Z7/cd_mean/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/Z7/cd_mean/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/Z7/CD mean Z7.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/Z7/excel_trend/cd_mean z7.xlsx')
    t = CdQcCdMeanZ7Calc(p, p_mid, p_from, search_plate=True)
    t.save_result_csv(p_csv)
    t.save_excels(p_save)
    t.save_excel_trend(p_trend)


