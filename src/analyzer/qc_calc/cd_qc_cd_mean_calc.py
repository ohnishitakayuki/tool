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
from cd_qc.cd_qc_cd_mean import CdQcCdMean


class CdQcCdMeanCalc(CdQcCalc):
    ignore_list_name = 'ignore_list.pkl'

    # Excel関係
    p_trend_format = Path(os.path.dirname(__file__) + '/../../excel_template/cdQC_trend/CD mean Trend.xlsx')
    excel_file_stem = 'CD_mean'
    excel_start_row = 6
    excel_start_column = 1

    # 測定ファイルの検索用
    search_word = '*.csv'
    search_meas_file = '**/*.csv'
    search_ref_file = '_all_'

    def __init__(self, p, p_mid=None, p_from=None, is_reload=False, search_plate=False, search_word=False):
        super().__init__(p, p_mid, p_from, is_reload, search_plate, search_word)

    def _get_meas_combination(self, list_meas_row):
        # CD refを探す関数。
        # 同一フォルダの'search_ref_file'が含まれているものをrefにする。
        # 2個以上あるときは一番新しいものを使用する。
        list_meas = []
        for list_meas_f in list_meas_row:
            p = Path(list_meas_f[1])
            file_name = p.name

            # refファイルの場合はスキップ
            if self.search_ref_file in file_name:
                continue

            # 最新のrefファイルを取得。
            m_date = None
            p_ref = None
            for f in p.parent.glob(f'*{self.search_ref_file}*'):
                m_date_tmp = datetime.fromtimestamp(f.stat().st_mtime)
                if m_date is None:
                    m_date = m_date_tmp
                    p_ref = f
                elif m_date_tmp > m_date:
                    m_date = m_date_tmp
                    p_ref = f

            # refファイルが無いときはスキップ
            if p_ref == None:
                continue

            # refファイルをリストに追加
            list_meas_tmp = list_meas_f + [str(p_ref)]
            list_meas.append(list_meas_tmp)
        return list_meas

    def _read_pickle(self, list_meas_set):
        # Nft Dynamicを読み込む
        c = CdQcCdMean(list_meas_set[1], list_meas_set[3], list_meas_set[2])
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
                            r.hor_50nm_space,
                            r.hor_200nm_space,
                            r.hor_500nm_space,
                            r.ver_50nm_space,
                            r.ver_200nm_space,
                            r.ver_500nm_space,
                            r.hor_50nm_pitch,
                            r.hor_200nm_pitch,
                            r.hor_500nm_pitch,
                            r.ver_50nm_pitch,
                            r.ver_200nm_pitch,
                            r.ver_500nm_pitch,
                        ]
        return list_result_tmp


if __name__ == '__main__':
    p = Path(os.path.dirname(__file__) + '/../../../data/E3640/cd_mean/')
    p_from = Path('//172.26.31.68/')
    p_mid = Path(os.path.dirname(__file__) + '/../../../mid_data/E3640/cd_mean/')
    p_save = Path(os.path.dirname(__file__) + '/../../../result/E3640/cd_mean/')
    p_csv = Path(os.path.dirname(__file__) + '/../../../result/E3640/CD mean.csv')
    p_trend = Path(os.path.dirname(__file__) + '/../../../result/excel/E3640/CD mean.xlsx')
    t = CdQcCdMeanCalc(p, p_mid, search_plate=True)
    t.save_result_csv(p_csv)
    # t.save_excels(p_save)
    # t.save_excel_trend(p_trend)


