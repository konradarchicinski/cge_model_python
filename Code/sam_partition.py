import pandas as pd
import os
import argparse
from pathlib import Path

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def sam_data_preparation(file_name, sheet_name, setting_file):
    '''
    Usually Social Accounting Matrix datasets are build in hard to operate way,
    this funtion helps to organize information from it.
    
    To prepare data for analysis user has to provide file name specific sheet name
    in it, with SAM table and setting file placed in Settings folder.
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
        features[column] = list(sf[column].dropna())
    tables = {
        'endowment_of_the_household': (features['factors'], features['households'][:-1]),
        'production_structure': (features['goods_activities'], features['factors']),
        'consumption_structure': (features['households'], features['goods_commodities']),
        #'government_consumption': (features['government'], features['goods_commodities']),
        'tax_revenue': (features['households'][:-1], features['inc_taxes']),
        'transfers': (features['households'][:-1], features['households'][:-1])
    }

    prep_data_folder = work_dir + '\\Data\\' + file_name.split('.')[0]
    
    if not os.path.exists(prep_data_folder):
        os.mkdir(prep_data_folder)

    activities = [good[1:] for good in features['goods_activities']]
    commodities = [good[1:] for good in features['goods_commodities']]

    for key, (col, row) in tables.items():
        table = micro[col].loc[row]
        if col == features['goods_activities']:
            table.columns = table.columns.str[1:] 
            for elem in list(set(commodities) - set(activities)):
                table[elem] = 0
        if col == features['goods_commodities']:
            table.columns = table.columns.str[1:]
            for elem in list(set(activities) - set(commodities)):
                table[elem] = 0
        if row == features['goods_activities']:
            table.index = table.index.str[1:]
            for elem in list(set(commodities) - set(activities)):
                table.loc[elem] = 0
        if row == features['goods_commodities']:
            table.index = table.index.str[1:]
            for elem in list(set(activities) - set(commodities)):
                table.loc[elem] = 0
        table.to_csv(
            prep_data_folder + '\\' + key + '.csv',
            header = True,
            na_rep = 0
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