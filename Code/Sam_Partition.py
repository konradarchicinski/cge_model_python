import pandas as pd
import numpy as np
import os
from pathlib import Path

# DATASET
#cwd = str(Path(os.getcwd()).parent)
cwd = os.getcwd()
macro = pd.read_excel(cwd + '\\Data\\SAM_Macro.xlsx',
                      header = 0)
macro = macro.drop(axis = 0, index = 0) #cleaning excel error
micro = pd.read_excel(cwd + '\\Data\\SAM_Micro.xlsx',
                      header = 0, index_col = 0)

# FACTORS
households = ['hhd-0', 'hhd-1', 'hhd-2', 'hhd-3', 'hhd-4', 'hhd-5', 'hhd-6', 'hhd-7', 'hhd-8',
              'hhd-91', 'hhd-92', 'hhd-93', 'hhd-94', 'hhd-95', 'gov']
factors = ['flab-p', 'flab-m', 'flab-s', 'flab-t', 'fcap']
taxes = ['atax', 'dtax', 'mtax', 'stax']
column_names = list(micro.columns)
goods_p = column_names[1:62]
goods_c = column_names[62:166]

def extract(df, file_name, r = None, c = None):
    if(r == None):
        df1 = df.loc[:,c]
        return df1.to_csv(cwd + '\\Data\\' + file_name + '.csv', na_rep = '-')
    elif(c == None):
        df1 = df.loc[r,:]
        return df1.to_csv(cwd + '\\Data\\' + file_name + '.csv', na_rep = '-')
    elif(r == None and c == None):
        return df.to_csv(cwd + '\\Data\\' + file_name + '.csv', na_rep = '-')
    else:
        df1 = df.loc[r,c]
        return df1.to_csv(cwd + '\\Data\\' + file_name + '.csv', na_rep = '-')
    
extract(micro, 'endowment', households, factors)
extract(micro, 'production', factors, goods_p)
extract(micro, 'consumption', goods_c, households)
extract(micro, 'taxes', taxes)