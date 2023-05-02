import argparse
from datetime import datetime
from modules import scatter, read_csv, general_stat

class Main:
  # init read parser arguments
  def __init__(self, parser) -> None:
    # args path of file
    parser.add_argument("--path", type=str, default="path", help="This is path of file")
    args = parser.parse_args()
    if args.path is None:
      print ("Please input path of file")
    if not "csv" and "xlsx" in args.path:
      print ("Please input file csv or xlsx")
    elif "csv" in args.path:
      print (args.path)
    elif "xlsx" in args.path:
      print (args.path)
    
    parser.add_argument("-s", type=str, metavar="S", default="scatter_plot", help="This is scatter plot")
    
    result = {}
    
    # sequence of function
    if "csv" in args.path:
      df = read_csv.read_csv(args.path)
    elif "xlsx" in args.path:
      df = read_csv.read_excel(args.path)
   
    result.update(general_stat.general_stat(df))
    
    date_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    # write file json
    with open (date_str + "_" + "data.json", "w") as f:
      f.write(result.to_json())
      

    

# if name == main
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Main")
  Main(parser)
