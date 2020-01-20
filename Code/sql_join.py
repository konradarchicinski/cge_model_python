import sqlite3
import pandas as pd
import argparse
import string
import os
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def sql_str(table_name, year_start, year_end):
    """Create a string for sql execution"""

    letters = list(string.ascii_lowercase)

    sql_str1 = "CREATE TABLE IF NOT EXISTS " + str(table_name) + " AS SELECT a.'index', " 
    sql_str2 = ""
    sql_str3 = ""
    sql_str4 = ""
    
    for i, year in enumerate(range(year_start, year_end+1)):
        if year != year_end:
            sql_str2 += letters[i] + ".'" + str(year) + "', " 
        else:
            sql_str2 += letters[i] + ".'" + str(year) + "' FROM "
        
    for i, year in enumerate(range(year_start, year_end)):
        if year == year_start:
            sql_str3 = "solution" + str(year) + " " + letters[i]
            sql_str4 += " left join solution" + str(year+1) + " " + letters[i+1] + " on a.'index'=" + letters[i+1] + ".'index'" 
        else:
            sql_str4 += " left join solution" + str(year+1) + " " + letters[i+1] + " on a.'index'=" + letters[i+1] + ".'index'" 
    
    sql_str = sql_str1 + sql_str2 + sql_str3 + sql_str4
    return sql_str


def join_tables(database, table_name="CompleteResults", year_start=2021, year_end=2025):
    """ Join tables inside a SQL database """
 
    conn = None
    conn = sqlite3.connect(
            work_dir + 
            '\\Data\\' 
            + database + '.db'
    )
    c = conn.cursor()
    c.execute(sql_str(table_name, year_start, year_end))
    conn.commit()
    conn.close() 

def main():
    parser = argparse.ArgumentParser(
        description='Program for joining SQL tables'
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
        Names created table in SQL Database.
        """,
    )
    parser.add_argument(
        'year_start', 
        type=int,
        nargs='?', 
        default=2021,
        help="""
        Year which begins the study.
        """,
    )
    parser.add_argument(
        'year_end', 
        type=int,
        nargs='?', 
        default=2025,
        help="""
        Year which closes the study.
        """,
    )    
    args = parser.parse_args()

    join_tables(args.database, args.table_name, args.year_start, args.year_end)    

if __name__ == '__main__':
    
    main()
    
