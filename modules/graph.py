import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


def main(data: pd.DataFrame):
    pass


def histogram(df: pd.DataFrame, save_dir: str, dict_result: dict):
    for col in df.columns:
        kde = True if df[col].dtype != "object" else False  # judge type of data
        fig, ax = plt.subplots(1, 1, dpi=300)
        ax = sns.histplot(data=df, x=col, kde=kde, color="blue", alpha=0.5)
        ax.set_title(col + " histogram")
        fig.savefig(save_dir + "/" + "hist_" + col + ".png")
        dict_result[col].update(
            {"histogram_save_path": save_dir + "/" + "hist_" + col + ".png"}
        )


def scatter_plot(df: pd.DataFrame, save_dir: str, dict_result: dict, columns: list):
    for x, y in columns:
        fig, ax = plt.subplots(1, 1, dpi=300)
        ax = sns.scatterplot(data=df, x=x, y=y, color="blue", alpha=0.5)
        ax.set_title(x + " scatter plot")
        fig.savefig(save_dir + "/" + "scatter_" + x + ".png")
        dict_result[x].update(
            {
                "vs_"
                + y
                + "_scatter_plot_save_path": save_dir
                + "/"
                + "scatter_"
                + x
                + ".png"
            }
        )


def cumulative_distribution_function(
    df: pd.DataFrame, save_dir: str, dict_result: dict
):
    for col in df.columns:
        if df[col].dtype != "object" and len(df[col].unique()) > len(df[col]) * 0.2:
            fx = stats.norm(loc=df[col].mean(), scale=df[col].std()).cdf(df[col])
            fig, ax = plt.subplots(1, 1, dpi=300)
            ax = sns.lineplot(data=df, x=col, y=fx, color="blue", alpha=0.5)
            ax.axvline(df[col].mean(), color="grey", linestyle="--")
            ax.set_title(col + " cumulative distribution function")
            fig.savefig(save_dir + "/" + "cdf_" + col + ".png")
            dict_result[col].update(
                {"cdf_save_path": save_dir + "/" + "cdf_" + col + ".png"}
            )


def qq_plot(df: pd.DataFrame, save_dir: str, dict_result: dict):
    for col in df.columns:
        if df[col].dtype != "object" and len(df[col].unique()) > len(df[col]) * 0.2:
            fig, ax = plt.subplots(1, 1, dpi=300)
            stats.probplot(df[col], dist="norm", plot=ax)
            ax.set_title(col + " qq plot")
            ax.get_lines()[1].set_alpha(0.5)
            ax.get_lines()[0].set_markersize(1)
            fig.savefig(save_dir + "/" + "qq_" + col + ".png")
            dict_result[col].update(
                {"qq_plot_save_path": save_dir + "/" + "qq_" + col + ".png"}
            )
