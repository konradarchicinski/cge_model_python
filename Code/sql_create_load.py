import sqlite3
from sqlite3 import Error
import pandas as pd
import os
import argparse
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def create_db(db_name, table_name):
    """ Create a Database, establish connection 
        and add a table to a Database """

    conn = None
    try:
        conn = sqlite3.connect(
            work_dir + 
            '\\Data\\Raw data\\' 
            + db_name + '.db'
        )
        if (table_name != None):
            table = pd.read_csv(
                work_dir + 
                '\\Data\\Raw data\\' 
                + table_name + '.csv'
            )
            table.to_sql(
                name=table_name, 
                if_exists='replace', 
                index=False,
                con=conn
            )
        
    except Error as e:
        print(e)
    finally:
        if conn:
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
        If second argument is blank then the database is created without any tables.
        """,
    )
    parser.add_argument(
        'table_name', 
        type=str,
        nargs='?', 
        default= None,
        help="""
        Specifies which .csv file from "Raw data" folder should be 
        loaded as a table to the database. This argument is optional.
        """
    )
    args = parser.parse_args()

    create_db(args.db_name, args.table_name)

if __name__ == '__main__':
    
    main()
    
