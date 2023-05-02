import pandas as pd

def general_stat(df:pd.DataFrame):
  df = df.describe()
  dict_df = df.to_dict()
  return dict_df
