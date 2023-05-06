import argparse
from datetime import datetime
import json
import pandas as pd
from modules import graph, read_csv, general_stat, relation_stat, ttest, read_xlsx
import os
import pathlib
from argparse import ArgumentParser
import textwrap
import glob
import shutil


class Main:
    # init read parser arguments
    def __init__(self, parser) -> None:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        # args path of file
        parser.add_argument(
            "--path", type=str, default="path", help="This is path of file"
        )
        help_text_method = """
        Method: default - all functions are process on each column.
                relation - relation analysis on each column
                ittest - independent t-test on 1st and 2nd columns or your input columns.
                pttest - paired t-test on 1st and 2nd column or your input columns.
                ottest - one-sample t-test on 1st column or your input column.
        """
        parser.add_argument(
            "--method",
            type=str,
            default="default",
            help=textwrap.dedent(help_text_method),
        )
        parser.add_argument(
            "-c", type=str, metavar="C", default="comment", help="This is comment"
        )
        parser.add_argument(
            "-sheet_name",
            type=str,
            default="Sheet1",
            help="This is sheet name of file xlsx",
        )  # args xlsx sheet name
        parser.add_argument(
            "-count",
            type=int,
            metavar="EA",
            default=10,
            help="Top N of categorical data",
        )  # general stat
        parser.add_argument(
            "-t1",
            type=str or int,
            default=0,
            help="test target column 1.",
        )
        parser.add_argument(
            "-t2",
            type=str or int,
            default=1,
            help="test target column 2.",
        )
        parser.add_argument(
            "-tc",
            type=str or list,
            default=[],
            help="Target divided categorical column.",
        )
        parser.add_argument(
            "-y",
            type=str,
            default="",
            help="y is dependent variable or target variable for relation analysis ",
        )
        parser.add_argument(
            "-d",
            type=str,
            default="",
            help="Caution: delete all files in public folder. If you want to delete, please input '-d delete'",
        )
        args = parser.parse_args()
        if args.d == "delete":
            judge = input("Are you sure to delete all files in public folder? (yes/no)")
            if "y" in judge:
                if not os.path.exists("public"):
                    print("public folder is not exist")
                    return
                files = glob.glob("public/*/")
                for f in files:
                    shutil.rmtree(f)
                print("delete all files in public folder")
                return
            else:
                print("cancel delete all files in public folder")
                return

        # check path of file
        if args.path is None:
            print("Please input path of file")
        if not "csv" and "xlsx" in args.path:
            print("Please input file csv or xlsx")
        elif "csv" in args.path:
            print(args.path)
        elif "xlsx" in args.path:
            print(args.path)

        dict_result = {}

        # sequence of general function
        if "csv" in args.path:
            df = read_csv.read_csv(args.path)
        elif "xlsx" in args.path:
            df = read_xlsx.read_xlsx(args.path, args.sheet_name)

        dict_result.update(general_stat.pick_up_key(df))  # columns name
        dict_result.update(
            general_stat.general_stat(df, count=args.count)
        )  # general stat

        # t1 and t2 replace to column name
        if not isinstance(args.t1, str):
            args.t1 = str(dict_result["columns_name"][args.t1])
        if not isinstance(args.t2, str):
            args.t2 = str(dict_result["columns_name"][args.t2])

        category_column = []

        # tc modify to list
        if "[" in args.tc:
            args.tc = args.tc.replace("[", "")
        if "]" in args.tc:
            args.tc = args.tc.replace("]", "")
        if "," in args.tc:
            args.tc = args.tc.split(",")
        for val in args.tc:
            if val.isdigit():
                category_column.append(int(val))
            else:
                category_column.append(val)

        # generate folder in public with os module
        date_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        save_dir = "public/" + date_str
        os.makedirs(save_dir, exist_ok=True)

        # comment
        comment = {"comment": args.c}
        dict_result.update(comment)

        # record file path
        file_path = {"file_path": args.path}
        dict_result.update(file_path)

        if args.method == "default":
            self.default_function(df, save_dir, dict_result)
        elif args.method == "relation":
            self.default_function(df, save_dir, dict_result)
            self.relation_function(df, save_dir, dict_result)
        elif args.method == "ittest":
            self.default_function(df, save_dir, dict_result)
            self.independent_t_test(df, save_dir, dict_result, args.t1, args.t2)
        elif args.method == "pttest":
            self.default_function(df, save_dir, dict_result)
            self.paired_t_test(df, save_dir, dict_result, args.t1, args.t2)
        elif args.method == "ottest":
            pass
        # closing sequence
        self.closing_function(save_dir, dict_result)

    """
    These are functions for main
    """

    def default_function(self, df, save_dir, dict_result):
        self.histogram(df, save_dir, dict_result)
        self.cumulative_plot(df, save_dir, dict_result)
        self.qq_plot(df, save_dir, dict_result)

    def relation_function(self, df, save_dir, dict_result):
        relation_stat.relation(
            df,
            save_dir,
            dict_result,
        )
        self.forest(df, save_dir, dict_result)

    def independent_t_test(self, df, save_dir, dict_result, t1, t2):
        ttest.independent_t_test(df, save_dir, dict_result, t1, t2)
        self.comparison_histogram(df, save_dir, dict_result, t1, t2)
        self.comparison_forest(df, save_dir, dict_result, t1, t2)

    def paired_t_test(self, df, save_dir, dict_result, t1, t2):
        ttest.paired_t_test(df, save_dir, dict_result, t1, t2)
        self.comparison_histogram(df, save_dir, dict_result, t1, t2)
        self.comparison_forest(df, save_dir, dict_result, t1, t2)

    """
    These are functions for default_function
    """

    def histogram(self, df, save_dir, dict_result):
        graph.histogram(df, save_dir, dict_result)
        
    def forest(self, df, save_dir, dict_result):
        graph.forest_plot(df, save_dir, dict_result)

    def comparison_histogram(self, df, save_dir, dict_result, t1, t2):
        graph.comparison_histogram(df, save_dir, dict_result, t1, t2)

    def comparison_forest(self, df, save_dir, dict_result, t1, t2):
        graph.forest_plot(df, save_dir, dict_result, t1, t2)

    def scatter_plot(self, df: pd.DataFrame):
        pass

    def cumulative_plot(self, df, save_dir, dict_result):
        graph.cumulative_distribution_function(df, save_dir, dict_result)

    def qq_plot(self, df, save_dir, dict_result):
        graph.qq_plot(df, save_dir, dict_result)

    """
    Following functions are for closing sequence
    """

    def closing_function(self, save_dir, dict_result):
        json_result = json.dumps(dict_result)
        with open(os.path.join(save_dir, "basic-stat-data.json"), "w") as f:
            f.write(json_result)

    def __del__(self):
        pass


# if name == main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main")
    main = Main(parser)
