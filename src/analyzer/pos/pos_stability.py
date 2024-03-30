import pandas as pd


class PosStability:
    def __init__(self, list_df):
        self.list_df = list_df

    def stab(self):
        df = pd.DataFrame()
        for df_tmp in self.list_df:
            df = pd.concat([df, df_tmp])
        df_all = df[['designX', 'designY', 'X', 'Y']].groupby(['designX', 'designY']).std().reset_index()
        df_all['X'] = df_all['X'] * 3
        df_all['Y'] = df_all['Y'] * 3
        stab_x = df_all['X'].max()
        stab_y = df_all['Y'].max()
        return stab_x, stab_y

    def meas_date(self):
        df = pd.DataFrame()
        for df_tmp in self.list_df:
            df = pd.concat([df, df_tmp])
        df['meas_date'] = pd.to_datetime(df['meas_date'])
        meas_date = df['meas_date'].max()
        return meas_date
