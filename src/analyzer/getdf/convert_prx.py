import numpy as np
import pandas as pd
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET


class ConvertPrx:
    file_ext = '.xml'
    def __init__(self, p):
        self.p = Path(p)

    def df(self, calc='symmetry'):
        with zipfile.ZipFile(self.p, 'r') as zf:
            # xmlファイルを探す関数。2個以上xmlファイルがあったとしても、1個目を対象。
            for f in zf.namelist():
                if self.file_ext in f:
                    p_xml = f
                    break

            root = ET.fromstring(zf.read(p_xml))

            if calc == 'symmetry' or calc == 'lpos':
                calc2 = 'symmetry'
                df = self._xml_parse_symmetry(root, calc2)
            elif calc == 'lpos_threshold':
                calc2 = 'lpos_threshold'
                df = self._xml_parse_lpos_threshold(root, calc2)
            else:
                return False
        return df

    def _xml_parse_symmetry(self, root, calc):
        i = 0
        pos_datas = []
        check_calc = 'symmetry'

        # XML解析はforループ回しでデータ取得する。かなり階層が深いのでネストだらけ。
        for Body in root.iter('Body'):
            for CaptureSites in Body.iter('CaptureSites'):
                for CaptureSite in CaptureSites.iter('CaptureSite'):
                    isSession = 0
                    pos_meas_time = np.nan
                    for Results in CaptureSite.iter('Results'):
                        for child4 in Results:
                            if child4.get('name') == 'Timestamp':
                                pos_meas_time_tmp = child4.text[:20]
                                pos_meas_time = pd.to_datetime(pos_meas_time_tmp)
                    for child in CaptureSite:
                        if child.tag == 'PositionX':
                            pos_screen_x = float(child.text)
                        if child.tag == 'PositionY':
                            pos_screen_y = float(child.text)
                        if child.text == 'session':
                            isSession = 1
                    for ParentDie in CaptureSite.iter('ParentDie'):
                        die_x = int(ParentDie.attrib['x'])
                        die_y = int(ParentDie.attrib['y'])
                    for Measurements in CaptureSite.iter('Measurements'):
                        if isSession == 0:
                            continue
                        for Measurement in Measurements.iter('Measurement'):
                            pos_dif_x = np.nan
                            pos_dif_y = np.nan
                            pos_meas_x = np.nan
                            pos_meas_y = np.nan
                            isMode = False

                            # モードチェック
                            for EvaluationMode in Measurement.iter('EvaluationMode'):
                                if EvaluationMode.text == check_calc:
                                    isMode = True
                            if not (isMode):
                                continue

                            for Rois in Measurement.iter('Rois'):
                                for Roi in Rois.iter('Roi'):
                                    for child2 in Roi:
                                        if child2.tag == 'PositionX':
                                            pos_roi_x = float(child2.text)
                                            pos_design_x = pos_screen_x + pos_roi_x
                                        if child2.tag == 'PositionY':
                                            pos_roi_y = float(child2.text)
                                            pos_design_y = pos_screen_y + pos_roi_y
                                    for Results in Roi.iter('Results'):
                                        for child3 in Results:
                                            if child3.get('name') == 'EdgesBF.1.DesignPosX':
                                                pos_meas_x = float(child3.text)
                                                pos_dif_x = (pos_meas_x - pos_design_x) * 1000
                                                pos_dif_xs = (pos_meas_x - pos_screen_x) * 1000
                                            if child3.get('name') == 'EdgesBF.2.DesignPosY':
                                                pos_meas_y = float(child3.text)
                                                pos_dif_y = (pos_meas_y - pos_design_y) * 1000
                                                pos_dif_ys = (pos_meas_y - pos_screen_y) * 1000

                            pos_data = [pos_design_x, pos_design_y, die_x, die_y , pos_dif_x, pos_dif_y,
                                        pos_dif_xs, pos_dif_ys, pos_roi_x, pos_roi_y, pos_meas_time]
                            i = i + 1
                            pos_datas.append(pos_data)

            df = pd.DataFrame(pos_datas, columns=['designX', 'designY', 'Row', 'Col', 'X', 'Y',
                                                      'screenX', 'screenY', 'fieldX', 'fieldY', 'meas_date'])
            return df



    def _xml_parse_lpos_threshold(self, root, calc):
        list_datas = []
        check_calc = 'threshold'

        # XML解析はforループ回しでデータ取得する。かなり階層が深いのでネストだらけ。
        for Body in root.iter('Body'):
            for CaptureSites in Body.iter('CaptureSites'):
                for CaptureSite in CaptureSites.iter('CaptureSite'):
                    isSession = 0
                    pos_meas_time = np.nan
                    for Results in CaptureSite.iter('Results'):
                        for child4 in Results:
                            if child4.get('name') == 'Timestamp':
                                pos_meas_time_tmp = child4.text[:20]
                                pos_meas_time = pd.to_datetime(pos_meas_time_tmp)
                    for child in CaptureSite:
                        if child.tag == 'PositionX':
                            pos_screen_x = float(child.text)
                        if child.tag == 'PositionY':
                            pos_screen_y = float(child.text)
                        if child.text == 'session':
                            isSession = 1
                    for ParentDie in CaptureSite.iter('ParentDie'):
                        die_x = int(ParentDie.attrib['x'])
                        die_y = int(ParentDie.attrib['y'])
                    for Measurements in CaptureSite.iter('Measurements'):
                        if isSession == 0:
                            continue
                        for Measurement in Measurements.iter('Measurement'):
                            isMode = False

                            # モードチェック
                            for EvaluationMode in Measurement.iter('EvaluationMode'):
                                if EvaluationMode.text == check_calc:
                                    isMode = True
                            if not(isMode):
                                continue

                            for Rois in Measurement.iter('Rois'):
                                for Roi in Rois.iter('Roi'):
                                    t_angle = ''
                                    for child2 in Roi:
                                        if child2.tag == 'PositionX':
                                            pos_roi_x = float(child2.text)
                                            pos_design_x = round(pos_screen_x + pos_roi_x, 4) * 1000
                                        if child2.tag == 'PositionY':
                                            pos_roi_y = float(child2.text)
                                            pos_design_y = round(pos_screen_y + pos_roi_y, 4) * 1000
                                        if child2.tag == 'Angle':
                                            if child2.text == '0':
                                                t_angle = 'X'
                                            elif child2.text == '90':
                                                t_angle = 'Y'
                                    v_data_edge = {}
                                    for Results in Roi.iter('Results'):
                                        pos_values = {}
                                        for child3 in Results:
                                            t_meas_result = child3.get('name')

                                            test_str = t_meas_result[-10:]
                                            if test_str == f'DesignPos{t_angle}':
                                                t_number_tmp = t_meas_result[:-11]
                                                t_number = int(t_number_tmp[8:])
                                                pos_meas = float(child3.text)
                                                if t_angle == 'X':
                                                    pos_dif = (pos_meas - pos_design_x / 1000) * 1000
                                                elif t_angle == 'Y':
                                                    pos_dif = (pos_meas - pos_design_y / 1000) * 1000
                                                pos_values[t_number] = pos_dif
                                        pos_value = (pos_values[1] + pos_values[2]) / 2
                                    v_data = {'designX': pos_design_x, 'designY': pos_design_y, 'Row': die_x,
                                              'Col': die_y, 'pos_value': pos_value, 'roi_angle': t_angle,
                                              'fieldX': pos_roi_x, 'fieldY': pos_roi_y, 'meas_date': pos_meas_time}
                                    v_datas = {**v_data, **v_data_edge}
                                    list_datas.append(v_datas)

            df = pd.DataFrame(list_datas)

            # XとYを同じ列に整頓
            df_x = df[df['roi_angle'] == 'X']
            df_y = df[df['roi_angle'] == 'Y']


            df_x = df_x.rename(columns={'pos_value': 'X'})
            df_y = df_y.rename(columns={'pos_value': 'Y'})
            df_y = df_y[['designX', 'designY', 'fieldX', 'fieldY', 'Y']]
            df = pd.merge(df_x, df_y, how='left', on=['designX', 'designY', 'fieldX', 'fieldY'])
            df = df[
                ['designX', 'designY', 'Row', 'Col', 'X', 'Y', 'fieldX', 'fieldY', 'meas_date']]
            return df


if __name__ == '__main__':
    p = Path('../../test/test_data/data_pos_qc_lpos_2k/LPOS35X35JINBEISL_2024-07-24_1_16-44-25.prx')
    # p = Path('../../test/test_data/data_convert_prx/LPOS35X35JINBEISL_2024-06-19_1_13-10-40.prx')
    t = ConvertPrx(p)
    df = t.df(calc = 'lpos_threshold')
    # df = t.df(calc='symmetry')
    # df = t.df()
    print(df)
    # df.to_csv('../../../t.csv')