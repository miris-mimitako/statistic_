import pandas as pd

def read_xlsx(path:str, sheet_name = "Sheet1")->pd.DataFrame:
  try:
    df = pd.read_excel(path, sheet_name=sheet_name)
  except:
    raise "sheet name is not exist"
  return df