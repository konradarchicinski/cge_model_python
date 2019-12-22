import pandas as pd
import os
import argparse
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def sam_data_preparation(file_name, sheet_name, setting_file):
    '''
    Usually Social Accounting Matrix datasets are build in hard to operate way,
    this funtion...

    To prepare data for analysis user has to...
    '''

    micro = pd.read_excel(
        work_dir + '\\Data\\Raw data\\' + file_name,
        sheet_name=sheet_name,
        header=0,
        index_col=0
    )
    sf = pd.read_excel(
        work_dir + '\\Settings\\' + setting_file,
        header=0
    )
    features = {}
    for column in sf:
        features[column] = sf[column].dropna()
    tables = {
        'endowment': (features['factors'], features['households']),
        'production': (features['goods_production'], features['factors']),
        'consumption': (features['households'], features['goods_consumption'])
    }

    for key, (col, row) in tables.items():
        table = micro[col].loc[row]
        table.to_csv(
            work_dir + '\\Data\\Raw data\\' + key + '.csv', 
            na_rep = '-'
        )


def main():
    
    parser = argparse.ArgumentParser(
        description='Program used for extracting data from Social Accounting Matrix.'
    )
    parser.add_argument(
        'file_name', 
        type=str,
        nargs='?', 
        default='SA_SAM_2015.xlsx', 
        help="""
        Capital shock variable in range between 0 and 1, 
        corresponding to the percentage decrease in the sector.
        """
    )
    parser.add_argument(
        'sheet_name',  
        type=str,
        nargs='?',
        default='Micro SAM 2015',
        help="""
        Labour shock variable in range between 0 and 1, 
        corresponding to the percentage decrease in the sector.
        """
    )
    parser.add_argument(
        'setting_file',  
        type=str,
        nargs='?',
        default='SA_setting.xlsx',
        help="""
        Labour shock variable in range between 0 and 1, 
        corresponding to the percentage decrease in the sector.
        """
    )
    args = parser.parse_args()

    sam_data_preparation(args.file_name, args.sheet_name, args.setting_file)


if __name__ == "__main__":

    main()
    