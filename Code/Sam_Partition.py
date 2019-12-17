import pandas as pd
import numpy as np

macro = pd.read_excel('C:/Users/Grzesiek/Desktop/Data Science/Python2019/Project/cge_model_python/Data/SAM_Macro.xlsx',
                      header = 0)
macro = macro.drop(axis = 0, index = 0) #cleaning excel error

micro = pd.read_excel('C:/Users/Grzesiek/Desktop/Data Science/Python2019/Project/cge_model_python/Data/SAM_Micro.xlsx',
                      header = 0, index_col = 0)

def extract(df, r = None, c = None):
    if(r == None):
        df1 = df.loc[:,c]
        return df1
    elif(c == None):
        df1 = df.loc[r,:]
        return df1
    elif(r == None and c == None):
        return df
    else:
        df1 = df.loc[r,c]
        return df1

# ENDOWMENT
households = ['hhd-0', 'hhd-1', 'hhd-2', 'hhd-3', 'hhd-4', 'hhd-5', 'hhd-6', 'hhd-7', 'hhd-8',
              'hhd-91', 'hhd-92', 'hhd-93', 'hhd-94', 'hhd-95', 'gov']
factors = ['flab-p', 'flab-m', 'flab-s', 'flab-t', 'fcap']
endowment = extract(micro, households, factors)
endowment.to_csv('C:/Users/Grzesiek/Desktop/Data Science/Python2019/Project/cge_model_python/Data/endowment.csv', na_rep = '-')

# PRODUCTION
column_names = list(micro.columns)
goods_p = column_names[1:62]
production = extract(micro, factors, goods_p)
production.to_csv('C:/Users/Grzesiek/Desktop/Data Science/Python2019/Project/cge_model_python/Data/production.csv', na_rep = '-')

# CONSUMPTION
column_names = list(micro.columns)
goods_c = column_names[62:166]
consumption = extract(micro, goods_c, households)
consumption.to_csv('C:/Users/Grzesiek/Desktop/Data Science/Python2019/Project/cge_model_python/Data/consumption.csv', na_rep = '-')

# TAX
taxes = ['atax', 'dtax', 'mtax', 'stax']
tax = extract(micro, taxes)
tax.to_csv('C:/Users/Grzesiek/Desktop/Data Science/Python2019/Project/cge_model_python/Data/tax.csv', na_rep = '-')
