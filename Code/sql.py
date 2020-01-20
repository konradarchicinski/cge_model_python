import sqlite3
from sqlite3 import Error
import pandas as pd
import os
import argparse
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def create_db(db_name):
    """ Create a Database, establish connection 
        and add a table to a Database """
    conn = None
    conn = sqlite3.connect(
            work_dir + 
            '\\Data\\' 
            + db_name + '.db'
    )
    def add_table():
        for filename in os.listdir(work_dir + "\\Data"):
            if filename.endswith(".csv"): 
                table = pd.read_csv(
                work_dir + 
                '\\Data\\' 
                + filename,
                skiprows = 1,
                names=["Year", filename[-8:-4]]            
                )
                table.to_sql(
                    name=filename, 
                    if_exists='replace', 
                    index=False,
                    con=conn
                ) 
    add_table()
    conn.close()
         
def main():
    parser = argparse.ArgumentParser(
        description='Program for SQL Database creation and adding tables to it'
    )
    parser.add_argument(
        'db_name', 
        type=str,
        nargs='?', 
        default='MyDatabase',
        help="""
        Creates a database of provided name if there isn't any db of the same name. 
        Iterates over all csv files provided in a folder.
        """,
    )
    args = parser.parse_args()

    create_db(args.db_name)    

if __name__ == '__main__':
    
    main()
    
