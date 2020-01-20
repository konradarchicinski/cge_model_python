import sqlite3
import os
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def sql_query(table_name, *args):
    """Query for specific variables from tables"""
    
    sql_query = "CREATE TABLE IF NOT EXISTS " + str(table_name) + "q" + " AS SELECT * FROM " + table_name + " q WHERE "
    
    if(len(args)) == 0:
        return None
    else:
        for arg in args:
            if arg != args[-1]:
                sql_query += "q.'index'='" + str(arg) + "' OR "
            else:
                sql_query += "q.'index'='" + str(arg) + "'"
    
    conn = None
    conn = sqlite3.connect(
            work_dir + 
            '\\Data\\' 
            + 'Database.db'
    )
    c = conn.cursor()
    c.execute(sql_query)
    conn.commit()
    conn.close()

#example
#sql_query("Table1","Gov_wealth", "Gov_PI")