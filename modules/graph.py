import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main(data: pd.DataFrame):
    pass

def histogram(df: pd.DataFrame, save_dir: str, dict_result: dict):
    for col in df.columns:
        kde = True if df[col].dtype != "object" else False  # judge type of data
        fig, ax = plt.subplots(1, 1, dpi=300)
        ax = sns.histplot(data=df, x=col, kde=kde, palette="winter", alpha=0.5)
        ax.set_title(col + " histogram")
        fig.savefig(save_dir + "/" + "hist_" + col + ".png")
        dict_result[col].update(
            {"histogram_save_path": save_dir + "/" + "hist_" + col + ".png"}
        )

def scatter_plot(df: pd.DataFrame, save_dir: str, dict_result: dict, columns: list):
    for x,y in columns:
        fig, ax = plt.subplots(1, 1, dpi=300)
        ax = sns.scatterplot(data=df, x=x, y=y, palette="winter", alpha=0.5)
        ax.set_title(x + " scatter plot")
        fig.savefig(save_dir + "/" + "scatter_" + x + ".png")
        dict_result[x].update(
            {"scatter_plot_save_path": save_dir + "/" + "scatter_" + x + ".png"}
        )
    
