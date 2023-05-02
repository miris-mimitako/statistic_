import argparse
from datetime import datetime
import json
import pandas as pd
from modules import graph, read_csv, general_stat
import os
import pathlib

class Main:
  # init read parser arguments
  def __init__(self, parser) -> None:
    # args path of file
    parser.add_argument("--path", type=str, default="path", help="This is path of file")
    parser.add_argument("--sheet_name", type=str, default="Sheet1", help="This is sheet name of file xlsx") # args xlsx sheet name
    parser.add_argument("-c", type=str, metavar="C", default="comment", help="This is comment")
    parser.add_argument("-s", type=str, metavar="S", default="scatter_plot", help="Generate scatter plot with numerical data")
    parser.add_argument("--count", type=int, metavar="EA", default=10, help="Top N of categorical data") # general stat
    
    args = parser.parse_args()
    if args.path is None:
      print ("Please input path of file")
    if not "csv" and "xlsx" in args.path:
      print ("Please input file csv or xlsx")
    elif "csv" in args.path:
      print (args.path)
    elif "xlsx" in args.path:
      print (args.path)
    
    dict_result = {}
    
    # sequence of function
    if "csv" in args.path:
      df = read_csv.read_csv(args.path)
    elif "xlsx" in args.path:
      df = read_csv.read_excel(args.path, args.sheet_name)
    
    dict_result.update(general_stat.pick_up_key(df)) # columns name
    dict_result.update(general_stat.general_stat(df, count=args.count)) # general stat
    
    # generate folder in public with os module
    date_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    save_dir = "public/" + date_str
    os.makedirs(save_dir, exist_ok=True)
    
    
    # comment
    comment = {"comment":args.c}
    dict_result.update(comment)
    
    # record file path
    file_path = {"file_path":args.path}
    dict_result.update(file_path)
    
    json_result = json.dumps(dict_result)
    
    
    # write file json
    with open (save_dir + "/" + "basic-stat-data.json", "w") as f:
      f.write(json_result)
    
    def histogram(df:pd.DataFrame, save_dir:str):
      graph.histogram(df, save_dir)
    
    def scatter_plot(df:pd.DataFrame):
      pass
    

# if name == main
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Main")
  Main(parser)
