
import numpy as np
import matplotlib.pyplot as plt


class NetGraph:
    """ ネットグラフ作成ツール
        __init__でdf、
        graphでpitch_size, グラフ名、セーブフォルダ指定
        セーブフォルダになにも指定しない場合はfig, axを返す
    """
    def __init__(self, df):
        self.df = df

    def graph(self, pitch_size, name, p_save=''):
        df = self.df
        pitch_size_text = pitch_size
        pitch_size = pitch_size
        # データ整頓
        # 　X, Yの要素数が合っているか確認
        column_names = df.columns.values
        df = df.sort_values(by=[column_names[0], column_names[1]])
        x_die_check = df.iloc[:, 0].nunique()
        y_die_check = df.iloc[:, 1].nunique()
        if x_die_check == 1:
            raise ValueError('X data is not even intervals')
        if y_die_check == 1:
            raise ValueError('Y data is not even intervals')
        # 3s計算してテキスト形式へ
        x_3s = df.iloc[:, 2].std() * 3
        y_3s = df.iloc[:, 3].std() * 3
        x_str = f'X {np.round(x_3s, 3)}nm'
        y_str = f'Y {np.round(y_3s, 3)}nm'

        # dfをnumpy2次元に変換
        x_die = df.iloc[:, 0].value_counts().iloc[0]
        y_die = df.iloc[:, 1].value_counts().iloc[1]
        x = df.iloc[:, 2].values.reshape(x_die, y_die)
        y = df.iloc[:, 3].values.reshape(x_die, y_die)
        x = x / pitch_size
        y = y / pitch_size

        # グリッドに合わせる行列作成
        rows, cols = np.meshgrid(range(x.shape[0]), range(x.shape[1]), indexing='ij')
        rows = rows + 1
        cols = cols + 1
        x = x + rows
        y = y + cols

        # グラフ作成
        plt.rcParams["font.size"] = 18
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        ax.plot(rows, cols, linestyle='None', marker='+', markersize=5, markeredgecolor='black')
        ax.plot([x.shape[0] - 1, x.shape[0] - 0], [0.5, 0.5], linewidth=0.5, color='black', marker='|', \
                markersize=5, markeredgecolor='black')
        graph_text = f'{pitch_size_text}nm'
        ax.text(x.shape[0] - 0.5, -0.5, graph_text, fontsize=15, horizontalalignment='center')
        ax.text(0.25, -0.05, x_str, fontsize=20, horizontalalignment='center', transform=ax.transAxes)
        ax.text(0.75, -0.05, y_str, fontsize=20, horizontalalignment='center', transform=ax.transAxes)
        for i in range(x.shape[0]):
            ax.plot(x[:, i], y[:, i], color='blue', linewidth=1)
        for i in range(y.shape[0]):
            ax.plot(x[i, :], y[i, :], color='blue', linewidth=1)
        ax.set_xlim(-1, x.shape[0] + 2)
        ax.set_ylim(-1, y.shape[0] + 2)
        ax.set_title(name, fontsize=18)
        ax.axis('off')
        if p_save == '':
            return fig, ax
        else:
            plt.savefig(p_save)