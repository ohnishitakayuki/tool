import numpy as np
import pandas as pd
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET


class ConvertPrx:
    file_ext = '.xml'
    def __init__(self, p):
        self.p = Path(p)

    def df(self):
        with zipfile.ZipFile(self.p, 'r') as zf:
            # xmlファイルを探す関数。1個目にしてしまう。
            for f in zf.namelist():
                if self.file_ext in f:
                    p_xml = f
                    break

            root = ET.fromstring(zf.read(p_xml))
            df = self._xml_parse(root)

    def _xml_parse(self, root):
        i = 0
        pos_datas = []
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
                    for Measurements in CaptureSite.iter('Measurements'):
                        if isSession == 0:
                            continue
                        for Measurement in Measurements.iter('Measurement'):
                            pos_dif_x = np.nan
                            pos_dif_y = np.nan
                            pos_meas_x = np.nan
                            pos_meas_y = np.nan
                            for Rois in Measurement.iter('Rois'):

                                for Roi in Rois.iter('Roi'):
                                    for child2 in Roi:
                                        if child2.tag == 'PositionX':
                                            pos_roi_x = float(child2.text)
                                            pos_design_x = round(pos_screen_x + pos_roi_x, 4)
                                        if child2.tag == 'PositionY':
                                            pos_roi_y = float(child2.text)
                                            pos_design_y = round(pos_screen_y + pos_roi_y, 4)
                                    for Results in Roi.iter('Results'):
                                        for child3 in Results:
                                            if child3.get('name') == 'EdgesBF.1.DesignPosX':
                                                pos_meas_x = float(child3.text)
                                                pos_dif_x = pos_meas_x - pos_design_x
                                            if child3.get('name') == 'EdgesBF.2.DesignPosY':
                                                pos_meas_y = float(child3.text)
                                                pos_dif_y = pos_meas_y - pos_design_y

                            pos_data = [pos_design_x, pos_design_y, pos_roi_x, pos_roi_y, pos_meas_x, pos_meas_y,
                                        pos_dif_x, pos_dif_y, pos_meas_time]
                            i = i + 1
                            print(pos_data)
            print (i)




            # root = ET.fromstring(result.read(p_file_xml))
            # list_tmp = list_get_data(root)


if __name__ == '__main__':
    p = Path('../../test/test_data/data_convert_prx/LPOS35X35JINBEISL_2024-06-19_1_13-10-40.prx')
    t = ConvertPrx(p)
    t.df()