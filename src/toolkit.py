"""Miscellanious functions used in the discography project."""

import matplotlib.font_manager as fm
import pandas as pd

def sql_to_string(sql_file_name):
    """Converts given SQL file contents to Python string."""
    with open('sql/{}'.format(sql_file_name), 'r') as file:
        sql_script = file.read()
    
    sql_string = '''\n{}\n'''.format(sql_script)
    return sql_string

def install_fonts():
    """Installs all fonts in the 'assets/font' folder."""
    font_dir = ['/assets/fonts']
    for font in fm.findSystemFonts(font_dir):
        fm.fontManager.addfont(font)

def sort_cat_column(df, column_name, cat_list):
    """Sorts categorical column by given list."""
    df[column_name] = pd.Categorical(df[column_name], cat_list)
    df.sort_values(column_name, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df