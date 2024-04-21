"""Miscellanious functions used in the discography project."""

import matplotlib.font_manager as fm
import pandas as pd

eras = ['Taylor Swift',
        'Fearless',
        'Speak Now',
        'Red',
        '1989',
        'reputation',
        'Lover',
        'folklore',
        'evermore',
        'Fearless (TV)',
        'Red (TV)',
        'Midnights',
        'Speak Now (TV)',
        '1989 (TV)',
        'TTPD',
        'Non-Album Songs',
        'Other Artist Songs']

def eras_order():
    return eras

def sql_to_string(sql_file_name):
    """Converts given SQL file contents to Python string."""
    with open('sql/{}'.format(sql_file_name), 'r') as file:
        sql_script = file.read()
    
    sql_string = '''\n{}\n'''.format(sql_script)
    return sql_string

def install_fonts():
    """Installs all fonts in the 'font' folder."""
    font_dir = ['/assets/fonts']
    for font in fm.findSystemFonts(font_dir):
        fm.fontManager.addfont(font)

def sort_cat_column(df, column_name, cat_list):
    """Sorts categorical column by given list."""
    df[column_name] = pd.Categorical(df[column_name], cat_list)
    df.sort_values(column_name, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def abbreviate_ttpd(df_column):
    """Abbreviates 'The Tortured Poets Department' to 'TTPD' to save space."""
    df_column = df_column.replace('The Tortured Poets Department', 'TTPD', inplace=True)
    return df_column

def chart_params(rcParams):
    """Setting the aesthetic parameters for the charts."""
    install_fonts()
    rcParams['font.family'] = 'Lato'
    rcParams['figure.dpi'] = 300
    rcParams['savefig.dpi'] = 150
    custom_params = {'ytick.left': True, 
                     'xtick.bottom': True}
    return rcParams, custom_params