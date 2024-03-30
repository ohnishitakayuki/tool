import numpy as np


class PosCorrect:
    def __init__(self, df):  # sw=0: translateのみ、sw=1: trans+rot, sw=2 1次
        self.df = df


    def correct_map(self, sw):
        df = self.df
        # Translation
        x_mean = df['X'].mean()
        y_mean = df['Y'].mean()
        df['X'] = df['X'] - x_mean
        df['Y'] = df['Y'] - y_mean

        if sw == 0:
            return df

        # Rotation
        if sw == 1:

            a1, _ = np.polyfit(df['designX'], df['X'], 1)
            a2, _ = np.polyfit(df['designY'], df['X'], 1)
            b1, _ = np.polyfit(df['designX'], df['Y'], 1)
            b2, _ = np.polyfit(df['designY'], df['Y'], 1)
            rot = (a2 - b1) / 2
            df['X'] = df['X'] - (df['designX'] - (df['designX'] * np.cos(rot) - df['designY'] * np.sin(rot)))
            df['Y'] = df['Y'] - (df['designY'] - (df['designX'] * np.sin(rot) + df['designY'] * np.cos(rot)))
            x_mean = df['X'].mean()
            y_mean = df['Y'].mean()
            df['X'] = df['X'] - x_mean
            df['Y'] = df['Y'] - y_mean
        elif sw == 2:
            x_mean = df['X'].mean()
            y_mean = df['Y'].mean()
            df['X'] = df['X'] - x_mean
            df['Y'] = df['Y'] - y_mean
            a1, _ = np.polyfit(df['designX'], df['X'], 1)
            a2, _ = np.polyfit(df['designY'], df['X'], 1)
            b1, _ = np.polyfit(df['designX'], df['Y'], 1)
            b2, _ = np.polyfit(df['designY'], df['Y'], 1)
            rot = (a2 - b1) / 2
            df['X'] = df['X'] - (df['designX'] * a1 + df['designY'] * a2)
            df['Y'] = df['Y'] - (df['designX'] * b1 + df['designY'] * b2)
            x_mean = df['X'].mean()
            y_mean = df['Y'].mean()
            df['X'] = df['X'] - x_mean
            df['Y'] = df['Y'] - y_mean

        return df