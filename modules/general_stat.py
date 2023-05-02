import pandas as pd

def general_stat(df:pd.DataFrame):
  df = df.describe()
  json_df = df.to_json()
  return json_df
