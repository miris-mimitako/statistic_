import pandas as pd
from scipy import stats
from modules import graph


def relation(df: pd.DataFrame, save_dir: str, dict_result: dict):
    list_num_column = []
    list_cat_column = []
    # judge type of data
    for col in df.columns:
        if df[col].dtype == "object":
            list_cat_column.append(col)
        elif len(df[col].unique()) < len(df[col]) * 0.2:
            list_cat_column.append(col)
        else:
            list_num_column.append(col)

    relation_numerical_data(df, list_num_column, list_cat_column, dict_result, save_dir)

    # make relation matrix


def relation_numerical_data(
    df: pd.DataFrame,
    list_num_column: list,
    list_cat_column: list,
    dict_result: dict,
    save_dir: str,
):
    r_df = df.copy()
    r_df.dropna(inplace=True)
    dict_result.update({"correlation": {}})
    for col in list_num_column:
        for col2 in list_num_column:
            if col == col2:
                continue
            else:
                r, p = stats.pearsonr(r_df[col], r_df[col2])
                dict_result["correlation"].update(
                    {col + "-" + col2: {"r": r, "r2": r**2, "p": p}}
                )

                graph.scatter_plot(df, save_dir, dict_result, [(col, col2)])
