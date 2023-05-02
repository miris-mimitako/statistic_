import pandas as pd

def read_csv(path:str)->pd.DataFrame:
  df = pd.read_csv(path)
  return df