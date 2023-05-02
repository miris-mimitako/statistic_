import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main(data:pd.DataFrame):
  pass

def histogram(df:pd.DataFrame, save_dir:str):
  for col in df.columns:
    fig, ax = plt.subplots(1,1, dpi=300)
    ax = sns.histplot(data=df, x=col, kde=True)
    fig.savefig(save_dir + "/" + col + ".png")
