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
            nan_count = df[key_name].isnull().sum()
            result[key_name].update({"count": int(len(df[key_name]) -int(nan_count))})
            result[key_name].update({"count_nan": int(nan_count)})
            result[key_name].update({"type": "categorical data"})
            result[key_name].update({"data_type": str(df[key_name].dtype)})

        elif "int" in str(df[key_name].dtype) or "float" in str(df[key_name].dtype):
            if len(df[key_name].unique()) < len(df[key_name]) * 0.2:
                result.update({key_name: {}})
                result[key_name].update({"item_list": {}})
                for x, y in df[key_name].value_counts().head(count).items():
                    result[key_name]["item_list"].update({x: y})
                nan_count = df[key_name].isnull().sum()
                result[key_name].update({"count": int(len(df[key_name]) -int(nan_count))})
                result[key_name].update({"count_nan": int(nan_count)})
                result[key_name].update({"type": "categorized numeric data"})
                result[key_name].update({"data_type": str(df[key_name].dtype)})
            else:
                result.update({key_name: {}})
                dict_df = df[key_name].describe().to_dict()
                result.update({key_name: dict_df})
                df_series = df[key_name].dropna()
                ci95 = stats.t.interval(
                    alpha=0.95,
                    df=len(df_series) - 1,
                    loc=df_series.mean(),
                    scale=stats.sem(df_series),
                )
                nan_count = df[key_name].isnull().sum()
                result[key_name].update({"ci95": ci95})
                if not nan_count:
                    result[key_name].update({"ci95_comment": "95% confidence interval is calculated from all data."})
                else:
                    result[key_name].update({"ci95_comment": "95% confidence interval is calculated from all data without Nan. Remove Nan with df.dropna()"})
                result[key_name].update({"ci95": ci95})
                result[key_name].update({"count_nan": int(nan_count)})
                result[key_name].update({"type": "numerical data"})
                result[key_name].update({"data_type": str(df[key_name].dtype)})

    print(result)
    return result


def pick_up_key(df: pd.DataFrame):
    list_key = df.columns.tolist()
    dict_key = {"columns_name": list_key}
    return dict_key
