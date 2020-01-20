import sqlite3
import os
from pathlib import Path
import argparse
import pandas as pd

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

# LIST VERSION
def sql_query(database, table_name, var_list):
    """Query for specific variables from tables"""
    
    if var_list == "All":
        sql_query = "SELECT * FROM " + table_name
    else:
        sql_query = "SELECT * FROM " + table_name + " t WHERE "
    
        if(len(var_list)) == 0:
            return None
        else:
            for var in var_list:
                if var != var_list[-1]:
                    sql_query += "t.'index'='" + str(var) + "' OR "
                else:
                    sql_query += "t.'index'='" + str(var) + "'"

    conn = None
    conn = sqlite3.connect(
            work_dir + 
            '\\Data\\' 
            + database +'.db'
    )
    data_table = pd.read_sql_query(sql_query, conn, index_col='index')
    del data_table.index.name
    conn.close()

    return data_table

# *ARGS VERSION 
# def sql_query(database, table_name, *args):
#     """Query for specific variables from tables"""
    
#     sql_query = sql_query = "SELECT * FROM " + table_name + " t WHERE "
    
#     if(len(args)) == 0:
#         return None
#     else:
#         for arg in args:
#             if arg != args[-1]:
#                 sql_query += "t.'index'='" + str(arg) + "' OR "
#             else:
#                 sql_query += "t.'index'='" + str(arg) + "'"
    
#     print(sql_query)
#     conn = None
#     conn = sqlite3.connect(
#             work_dir + 
#             '\\Data\\' 
#             + database +'.db'
#     )
#     return pd.read_sql_query(sql_query, conn)
#     conn.close()
# example
# sql_query("DB1", "Table1", "Gov_wealth", "Gov_PI")

def main():
    parser = argparse.ArgumentParser(
         description='Program for SQL queries'
    )
    parser.add_argument(
        'database', 
        type=str,
        nargs='?', 
        default='Database',
        help="""
        Creates a database of provided name if there isn't any db of the same name. 
        If there is one then performs operations on it.
        """,
    )
    parser.add_argument(
        'table_name', 
        type=str,
        nargs='?', 
        default='CompleteResults',
        help="""
        Name of a table in SQL Database.
        """,
    )
    parser.add_argument(
        'var_list',
        metavar='N',
        nargs='*',
        type=str, 
        help="""List of variables to be shown on graph""",     
    )
    args = parser.parse_args()
    
    sql_query(args.database, args.table_name, args.var_list)    

if __name__ == '__main__':
    
    main()