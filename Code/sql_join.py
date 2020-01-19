import sqlite3
import pandas as pd
import argparse
import string
import os
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def sql_str(year_start, year_end):
    """Create a string for sql execution"""

    letters = list(string.ascii_lowercase)
    
    sql_str1 = "CREATE TABLE solution" + str(year_start) + str(year_end) + " AS SELECT a.'index', " 
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


def join_tables(database):
    """ Join tables inside a SQL database """
    
    conn = None
    conn = sqlite3.connect(
            work_dir + 
            '\\Data\\' 
            + database + '.db'
    )
    c = conn.cursor()
    
    string = sql_str(2021,2025)
    c.execute(string)
    # c.execute("CREATE TABLE solutionAll5 AS SELECT a.'index', a.'2021', b.'2022', c.'2023' FROM solution2021 a left join solution2022 b on a.'index'=b.'index' \
    #      left join solution2023 c on a.'index'=c.'index'")
        
    conn.commit()
    conn.close() 

def main():
    parser = argparse.ArgumentParser(
        description='Program for SQL Database creation and adding tables to it'
    )
    parser.add_argument(
        'database', 
        type=str,
        nargs='?', 
        default='Database',
        help="""
        Creates a database of provided name if there isn't any db of the same name. 
        If second argument is blank then the database is created without any tables.
        """,
    )
    args = parser.parse_args()

    join_tables(args.database)    

if __name__ == '__main__':
    
    main()
    
