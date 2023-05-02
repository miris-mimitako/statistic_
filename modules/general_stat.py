import pandas as pd
from scipy import stats


def general_stat(df: pd.DataFrame, count=10):
    key = df.columns.tolist()
    result = {}
    for key_name in key:
        if df[key_name].dtype == "object":
            result.update({key_name: {}})
            result[key_name].update({"item_list": {}})
            for x, y in df[key_name].value_counts().head(count).items():
                result[key_name]["item_list"].update({x: y})
            result[key_name].update({"type": "categorical"})

        elif df[key_name].dtype == "int64" or df[key_name].dtype == "float64":
            result.update({key_name: {}})
            dict_df = df[key_name].describe().to_dict()
            result.update({key_name: dict_df})
            # df[key_name].dropna(inplace=True)
            df_series = df[key_name].dropna()
            # ci95 = stats.t.interval(alpha=0.95, df=len(df[key_name])-1, loc=df[key_name].mean(), scale=stats.sem(df[key_name]))
            ci95 = stats.t.interval(
                alpha=0.95,
                df=len(df_series) - 1,
                loc=df_series.mean(),
                scale=stats.sem(df_series),
            )
            result[key_name].update({"ci95": ci95})
            result[key_name].update({"type": "numerical"})

    return result


def pick_up_key(df: pd.DataFrame):
    list_key = df.columns.tolist()
    dict_key = {"columns_name": list_key}
    return dict_key
