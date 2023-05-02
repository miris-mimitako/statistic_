import pandas as pd

def general_stat(df:pd.DataFrame):
  df = df.describe()
  dict_df = df.to_dict()
  return dict_df

def pick_up_key(df:pd.DataFrame):
  list_key = df.columns.tolist()
  dict_key = {"columns_name":list_key}
  return dict_key