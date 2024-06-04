import pandas as pd 
import numpy as np
import os 
from datetime import datetime



def schedule_generator(df, export_file='eclipse_schedule', export_folder=".", injection=False, production=True):
    """ function to generate the schedule file for eclipse

    Args:
        df (_type_): dataframe containing the data format is ['FOPR', 'FGPR', 'FWPR', 'FIELD', 'MOTHER_FIELD']
        export_file (str, optional): file to be exported. Defaults to 'eclipse_schedule.sch'.
        injection (bool, optional): if True, the schedule will be generated for injection. Defaults to False.
    """
    eclipse_date ={1:'JAN',2:'FEB',3:'MAR',\
    4:'APR',5:'MAY',6:'JUN',7:'JUL',\
        8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_export_file = f"{export_file}_{current_time}.sch"
    os.makedirs(export_folder, exist_ok=True)
    file_path = os.path.join(export_folder, new_export_file)
    with open(file_path, "w") as f:
        f.write("------------------------------------------\n")
        f.write("-- Automatic generation of the GRUPTREE --\n")
        f.write("GRUPTREE \n")
        for field in df['FIELD'].unique():
           f.write(f" '{field}'       '{df.loc[df.FIELD==field, 'MOTHER_FIELD'].unique()[0]}' / --fields to be tied in to FIELD \n")
        f.write("/ \n")

        f.write("------------------------------------------\n")
        f.write("-- Automatic generation of the GSATPROD --\n")
        f.write("-- Based on dummy exports-- \n")
        f.write("------------------------------------------------ \n")
        for selected_date in df.index.unique():
            f.write("DATES \n")
            f.write(f"{selected_date.day}  {eclipse_date[selected_date.month]}  {selected_date.year}  / \n")
            f.write("/ \n")
            f.write("GSATPROD \n")
            for field in df.FIELD.unique():
                if not (df.loc[(df.index == selected_date)&(df.FIELD == field)]).empty :
                    oil = df.loc[(df.index == selected_date) &(df.FIELD == field), 'FOPR'].values[0]
                    gas = df.loc[(df.index == selected_date) &(df.FIELD == field), 'FGPR'].values[0]
                    water = df.loc[(df.index == selected_date) &(df.FIELD == field), 'FWPR'].values[0]                    
                    f.write(f"'{field}'  {oil:.2f}  {gas:.2f}  {water:.2f}  3*  / \n")
            f.write("/ \n")
        return file_path
        print("file generated")
