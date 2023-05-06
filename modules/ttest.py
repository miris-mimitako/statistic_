from scipy import stats
import numpy as np
import pandas as pd


def independent_t_test(df, save_dir, dict_result, t1, t2):
    x1 = df[t1].dropna() if isinstance(t1, str) else df.iloc[:, t1].dropna()
    x2 = df[t2].dropna() if isinstance(t2, str) else df.iloc[:, t2].dropna()
    t_stat, p_val = stats.ttest_ind(x1, x2, equal_var=False)
    x1_average = np.mean(x1)
    x2_average = np.mean(x2)
    x1_std = np.std(x1, ddof=1)  # unbiased std
    x2_std = np.std(x2, ddof=1)  # unbiased std
    d = (x1_average - x2_average) / np.sqrt((x1_std**2 + x2_std**2) / 2)

    if isinstance(t1, str) and isinstance(t2, str):
        dict_result.update(
            {"independent_t_test": {t1 + "-" + t2: {"t_stat": t_stat, "p_val": p_val}}}
        )
        dict_result["independent_t_test"].update(
            {"mean": {str(t1): float(np.mean(x1)), str(t2): float(np.mean(x2))}}
        )
        dict_result["independent_t_test"].update(
            {"std": {str(t1): float(np.std(x1)), str(t2): float(np.std(x2))}}
        )
        dict_result["independent_t_test"].update({"d": d})
        dict_result["independent_t_test"].update({"N": {t1: len(x1), t2: len(x2)}})

    else:
        dict_result.update(
            {"independent_t_test": {"column_0-1": {"t_stat": t_stat, "p_val": p_val}}}
        )
        dict_result["independent_t_test"].update(
            {"mean": {str(t1): float(np.mean(x1)), str(t2): float(np.mean(x2))}}
        )
        dict_result["independent_t_test"].update(
            {"std": {str(t1): float(np.std(x1)), str(t2): float(np.std(x2))}}
        )
        dict_result["independent_t_test"].update({"d": d})
        dict_result["independent_t_test"].update({"N": {"0": len(x1), "1": len(x2)}})


def paired_t_test(df, save_dir, dict_result, t1, t2):
    x1 = df[t1].dropna() if isinstance(t1, str) else df.iloc[:, t1].dropna()
    x2 = df[t2].dropna() if isinstance(t2, str) else df.iloc[:, t2].dropna()
    t_stat, p_val = stats.ttest_rel(x1, x2)
    x1_average = np.mean(x1)
    x2_average = np.mean(x2)
    x1_std = np.std(x1, ddof=1)  # unbiased std
    x2_std = np.std(x2, ddof=1)  # unbiased std
    d = (x1_average - x2_average) / np.sqrt((x1_std**2 + x2_std**2) / 2)

    if isinstance(t1, str) and isinstance(t2, str):
        dict_result.update(
            {
                "paired_t_test": {
                    t1
                    + "-"
                    + t2: {
                        "t_stat": t_stat,
                        "p_val-Two_tailed_test)": p_val,
                        "p_val-One_tailed_test)": p_val / 2,
                    }
                }
            }
        )
        dict_result["paired_t_test"].update(
            {"mean": {str(t1): float(np.mean(x1)), str(t2): float(np.mean(x2))}}
        )
        dict_result["paired_t_test"].update(
            {"std": {str(t1): float(np.std(x1)), str(t2): float(np.std(x2))}}
        )
        dict_result["paired_t_test"].update({"d": d})
        dict_result["paired_t_test"].update({"N": {t1: len(x1), t2: len(x2)}})

    else:
        dict_result.update(
            {
                "paired_t_test": {
                    "column_0-1": {
                        "t_stat": t_stat,
                        "p_val-Two_tailed_test)": p_val,
                        "p_val-One_tailed_test)": p_val / 2,
                    }
                }
            }
        )
        dict_result["paired_t_test"].update(
            {"mean": {str(t1): float(np.mean(x1)), str(t2): float(np.mean(x2))}}
        )
        dict_result["paired_t_test"].update(
            {"std": {str(t1): float(np.std(x1)), str(t2): float(np.std(x2))}}
        )
        dict_result["paired_t_test"].update({"d": d})
        dict_result["paired_t_test"].update({"N": {"0": len(x1), "1": len(x2)}})
