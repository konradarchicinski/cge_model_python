import sqlite3
import os
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def sql_query1(table_name, *args):
    """Query for specific variables from tables"""
    
    sql_temp = "CREATE TABLE IF NOT EXISTS " + str(table_name) + "q" + " AS SELECT * FROM " + table_name + " WHERE 1=2"
    sql_query = "INSERT INTO " + str(table_name) + "q" + " SELECT * FROM " + table_name + " WHERE "
    
    if(len(args)) == 0:
        return None
    else:
        for arg in args:
            if arg != args[-1]:
                sql_query += "'index'=" + str(arg) + " OR "
            else:
                sql_query += "'index'=" + str(arg)
    
    conn = None
    conn = sqlite3.connect(
            work_dir + 
            '\\Data\\' 
            + 'Database.db'
    )
    c = conn.cursor()
    # string = sql_query("solution20212024","\'Gov_wealth\'","\'Gov_PI\'")
    # print(string)
    print(sql_temp, "\n", sql_query)
    c.execute(sql_temp)
    conn.commit()
    c.execute(sql_query)
    conn.commit()
    conn.close()



sql_query1("solution20212023","\"Gov_wealth\"","\"Gov_PI\"")
