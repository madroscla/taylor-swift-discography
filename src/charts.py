"""Builds charts in seaborn/matplotlib."""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

def credit_chart(color_dict, custom_params, plot_type, df, x_values, y_values, 
                 hues, avg_series, title, x_label, y_label, legend_title, rotate_x, 
                 save_png=False, png_name=None, table_bool=False, table_df=None):
    """Build musician credit chart based on given arguments.

       Args:
           color_dict: dict, {'category': 'hex color'}
           custom_params: dict, matplotlib custom params
           plot_type: str, 'bar' or 'line'
           df: pandas dataframe
           x_values: series, column in df
           y_values: series, column in df
           hues: series, column in df
           avg_series: series, averages per hues
           title: str, chart title
           x_label: str, x-axis label
           y_label: str, y-axis label
           legend_title: str, title for legend
           rotate_x: bool, rotates x tick labels
           save_png: bool, default False, saves chart to png
           png_name: str, default None, image name (must include .png)
           table_bool: bool, default False, includes values table
           table_df: formatted df, default None, needed for table 
    """
    palette = sns.color_palette(color_dict.values())
    sns.set_theme(style='darkgrid', rc=custom_params)
    fig, ax = plt.subplots(figsize=(17, 5))
    
    bbox_tup = ()
    match plot_type:
        case 'bar':
            bbox_tup = (0, -0.4, 1, 0.2)
        case 'line':
            bbox_tup = (0.018, -0.4, .97, 0.2)
    
    # Creating barplot and drawing average lines
    if plot_type == 'bar':
        sns.barplot(df, x=x_values, y=y_values, hue=hues, errorbar=None, ax=ax, palette=palette)
    elif plot_type == 'line':
        sns.lineplot(df, x=x_values, y=y_values, hue=hues, style=hues, 
                 markers=True, dashes=False, ax=ax, palette=palette)
        
    for (type, avg) in avg_series.items():
        plt.axhline(y=avg, color=color_dict[type], linestyle='--', 
                    label='{} (avg)'.format(type), alpha=0.5)

    if table_bool == True:
        plt.table(cellText=table_df.values, cellLoc='center', 
                  rowLabels=table_df.index, rowColours=list(color_dict.values()),
                  bbox=bbox_tup)
        plt.xlabel(x_label, fontweight='bold', fontsize='medium',
               labelpad=80)
    else:
        plt.xlabel(x_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    
    plt.title(title, 
              fontweight='bold', fontsize='x-large')
    plt.ylabel(y_label, fontweight='bold', fontsize='medium', 
               labelpad=5.5)
    plt.legend(title=legend_title)
    if rotate_x == True:
        ax.tick_params(axis='x', labelrotation=20)

    if save_png == True:
        plt.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')

def collab_heatmap(custom_params, df, x_values, y_values, value_field, title, x_label, y_label, 
                   rotate_x, save_png=False, png_name=None, table_bool=False, table_df=None):
    """Build collaborator heatmap based on given arguments.

       Args:
           custom_params: dict, matplotlib custom params
           df: pandas dataframe
           x_values: series, column in df
           y_values: series, column in df
           value_field: series, column in df, cells in pivoted df
           title: str, chart title
           x_label: str, x-axis label
           y_label: str, y-axis label
           rotate_x: bool, rotates x tick labels
           save_png: bool, default False, saves chart to png
           png_name: str, default None, image name (must include .png)
           table_bool: bool, default False, includes values table
           table_df: formatted df, default None, needed for table 
    """
    sns.set_theme(style='darkgrid', rc=custom_params)
    fig, ax = plt.subplots(figsize=(17, 10))

    df_pivot = df.pivot_table(index=y_values, columns=x_values, values=value_field, fill_value=0, 
                              aggfunc='sum', observed=False)
    df_pivot.sort_values(y_values, inplace=True)
    
    sns.heatmap(df_pivot, annot=True, linewidths=1.5, linecolor='#FFFFFF', ax=ax, cmap='PuRd', cbar=False)

    if table_bool == True:
        table = plt.table(cellText=table_df.values, cellLoc='center', 
                  colLabels=['Totals'], edges='vertical',
                  bbox=(1.01, 0.003, 0.06, 1.08))
        for (row, col), cell in table.get_celld().items():
            if (row == 0):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))
        
    plt.title(title, 
              fontweight='bold', fontsize='x-large')
    plt.xlabel(x_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    plt.ylabel(y_label, fontweight='bold', fontsize='medium', 
               labelpad=5.5)
    if rotate_x == True:
        ax.tick_params(axis='x', labelrotation=40)

    if save_png == True:
        plt.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')