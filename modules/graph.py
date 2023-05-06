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


def comparison_histogram(df, save_dir: str, dict_result: dict, t1: str, t2: str):
    fig, ax = plt.subplots(1, 1, dpi=300)
    ax = sns.histplot(data=df, x=t1, kde=True, color="blue", alpha=0.5, legend=True)
    ax = sns.histplot(data=df, x=t2, kde=True, color="red", alpha=0.5, legend=True)
    ax.set_title(t1 + "and " + t2 + " histogram")
    fig.savefig(save_dir + "/" + "comparison_hist_" + t1 + "_and_" + t2 + ".png")
    dict_result.update(
        {
            "comparison_histogram_save_path": save_dir
            + "/"
            + "comparison_hist_"
            + t1
            + "_and_"
            + t2
            + ".png"
        }
    )


def forest_plot(df: pd.DataFrame, save_dir: str, dict_result: dict, t1="", t2=""):
    if t1 and t2:
        df_c = df.copy()
        df_c["t1_title"] = t1
        df_c["t2_title"] = t2
        df_melted = pd.melt(
            df_c,
            id_vars=["t1_title", "t2_title"],
            value_vars=[t1, t2],
            var_name="column_name",
            value_name="value",
        )
        # create forest plot
        fig, ax = plt.subplots(1, 1, dpi=300)
        ax = sns.pointplot(
            data=df_melted,
            x="value",
            y="column_name",
            errorbar=("ci", 95),
            capsize=0.2,
            join=False,
            color="blue",
            errwidth=0.5,
        )
        ax.set_title(t1 + " and " + t2 + " forest plot with 95% confidence interval")
        fig.savefig(save_dir + "/" + "forest_plot_" + t1 + "_and_" + t2 + ".png")
        dict_result.update(
            {
                "forest_plot_save_path": save_dir
                + "/"
                + "forest_plot_"
                + t1
                + "_and_"
                + t2
                + ".png"
            }
        )
    else:
        # create forest plot
        df_c = df.copy()
        fig, ax = plt.subplots(1, 1, dpi=300)
        list_melt_colum = []
        list_melt_value = []
        for col in df.columns:
            if df[col].dtype != "object" and len(df[col].unique()) > len(df[col]) * 0.2:
                df_c[col + "_"] = col
                list_melt_colum.append(col + "_")
                list_melt_value.append(col)

        else:
            df_melted = pd.melt(
                df_c,
                id_vars=list_melt_colum,
                value_vars=list_melt_value,
                var_name="column_name",
                value_name="value",
            )
            fig, ax = plt.subplots(1, 1, dpi=300)
            ax = sns.pointplot(
                data=df_melted,
                x="value",
                y="column_name",
                errorbar=("ci", 95),
                capsize=0.2,
                join=False,
                color="blue",
                errwidth=0.5,
            )
            ax.set_title(
                t1 + " and " + t2 + " forest plot with 95% confidence interval"
            )
            fig.savefig(save_dir + "/" + "forest_plot.png")
            dict_result.update(
                {"forest_plot_save_path": save_dir + "/" + "forest_plot" + ".png"}
            )

            # ax = sns.pointplot(
            #     data=df,
            #     x=col,
            #     y=str(col),
            #     errorbar=("ci", 95),
            #     capsize=0.4,
            #     join=False,
            #     color=".5",
            # )


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


def grouped_scatter_plot(
    df: pd.DataFrame, save_dir: str, dict_result: dict, columns: list, hue: str
):
    x, y = columns
    fig, ax = plt.subplots(1, 1, dpi=300)
    ax = sns.scatterplot(data=df, x=x, y=y, hue=hue, palette="winter", alpha=0.5)
    ax.set_title(x + " grouped scatter plot with " + hue)
    fig.savefig(save_dir + "/" + "grouped_scatter_" + x + "_with_" + hue + ".png")
    dict_result[x].update(
        {
            "vs_"
            + y
            + "_grouped_scatter_plot_save_path": save_dir
            + "/"
            + "grouped_scatter_"
            + x
            + "_with_"
            + hue
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
