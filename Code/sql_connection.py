import sqlite3
from sqlite3 import Error
import pandas as pd
import os
import argparse
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def create_connection(db_name):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(
            work_dir + 
            '\\Data\\Raw data\\' 
            + db_name + '.db'
        )
        #c = conn.cursor()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def main():
    parser = argparse.ArgumentParser(
        description='Program for SQL database creation'
    )
    parser.add_argument(
        'db_name', 
        type=str,
        nargs='?', 
        default='MyDatabase'
    )
    args = parser.parse_args()
    
    create_connection(args.db_name)
    

if __name__ == '__main__':
    
    main()
    
