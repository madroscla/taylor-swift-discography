"""Builds charts in seaborn/matplotlib."""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker
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
           x_values: str, column name in df
           y_values: str, column name in df
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
    sns.set_theme(style='white', rc=custom_params)
    fig, ax = plt.subplots(figsize=(17, 5))
    fig.patch.set_facecolor('#EDECE8')
    
    bbox_tup = ()
    match plot_type:
        case 'bar':
            bbox_tup = (0, -0.4, 1, 0.2)
        case 'line':
            bbox_tup = (0.018, -0.4, .97, 0.2)
    
    # Creating barplot and drawing average lines
    if plot_type == 'bar':
        sns.barplot(data=df, x=x_values, y=y_values, hue=hues, errorbar=None, ax=ax, palette=palette)
    elif plot_type == 'line':
        sns.lineplot(data=df, x=x_values, y=y_values, hue=hues, style=hues, 
                 markers=True, dashes=False, ax=ax, palette=palette)
        
    for (collab_type, avg) in avg_series.items():
        ax.axhline(y=avg, color=color_dict[collab_type], linestyle='--', 
                    label='{} (avg)'.format(collab_type), alpha=0.5)

    if table_bool == True:
        ax.table(cellText=table_df.values, cellLoc='center', 
                  rowLabels=table_df.index, rowColours=list(color_dict.values()),
                  bbox=bbox_tup)
        ax.set_xlabel(x_label, fontweight='bold', fontsize='medium',
               labelpad=80)
    else:
        ax.set_xlabel(x_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    
    ax.set_title(title, 
              fontweight='bold', fontsize='x-large')
    ax.set_ylabel(y_label, fontweight='bold', fontsize='medium', 
               labelpad=5.5)
    ax.legend(title=legend_title)
    if rotate_x == True:
        ax.tick_params(axis='x', labelrotation=20)

    if save_png == True:
        fig.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')

    return fig, ax

def collab_heatmap(custom_params, df, x_values, y_values, value_field, aggfunc, title, x_label, y_label, 
                   rotate_x, save_png=False, png_name=None, table_bool=False, table_df=None):
    """Build collaborator heatmap based on given arguments.

       Args:
           custom_params: dict, matplotlib custom params
           df: pandas dataframe
           x_values: str, column name in df
           y_values: str, column name in df
           value_field: series, column in df, cells in pivoted df
           aggfunc: str, aggregate function for pivoted df
           title: str, chart title
           x_label: str, x-axis label
           y_label: str, y-axis label
           rotate_x: bool, rotates x tick labels
           save_png: bool, default False, saves chart to png
           png_name: str, default None, image name (must include .png)
           table_bool: bool, default False, includes values table
           table_df: formatted df, default None, needed for table 
    """
    sns.set_theme(style='white', rc=custom_params)
    fig, ax = plt.subplots(figsize=(17, 10))
    fig.patch.set_facecolor('#EDECE8')

    df_pivot = df.pivot_table(index=y_values, columns=x_values, values=value_field, fill_value=0, 
                              aggfunc=aggfunc, observed=False)
    df_pivot.sort_values(y_values, inplace=True)
    
    sns.heatmap(df_pivot, annot=True, linewidths=1.5, linecolor='#FFFFFF', ax=ax, cmap='PuRd', cbar=False)

    if table_bool == True:
        table = ax.table(cellText=table_df.values, cellLoc='center', 
                  colLabels=['Totals'], edges='vertical',
                  bbox=(1.01, 0.003, 0.06, 1.08))
        for (row, col), cell in table.get_celld().items():
            if (row == 0):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))
        
    ax.set_title(title, 
              fontweight='bold', fontsize='x-large')
    ax.set_xlabel(x_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    ax.set_ylabel(y_label, fontweight='bold', fontsize='medium', 
               labelpad=5.5)
    if rotate_x == True:
        ax.tick_params(axis='x', labelrotation=40)

    if save_png == True:
        plt.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')

    return fig, ax

def formats_pie(custom_params, df, wedge_values, wedge_labels, title, colors_list, 
                save_png=False, png_name=None, table_bool=False, table_df=None):
    """Build collaborator heatmap based on given arguments.

       Args:
           custom_params: dict, matplotlib custom params
           df: pandas dataframe
           wedge_values: str, column name in df
           wedge_labels: str, column name in df
           title: str, chart title
           colors_list: list, colors for wedges
           save_png: bool, default False, saves chart to png
           png_name: str, default None, image name (must include .png)
           table_bool: bool, default False, includes values table
           table_df: formatted df, default None, needed for table 
    """
    sns.set_theme(style='white', rc=custom_params)
    fig, ax = plt.subplots(figsize=(17, 5))
    fig.patch.set_facecolor('#EDECE8')
    ax.pie(df[wedge_values], autopct='%1.1f%%', colors=colors_list, 
           wedgeprops={"edgecolor":"#132a13"}, textprops={"fontsize":9})
    ax.set_title(title, fontweight='bold', fontsize='large', x=0.77)
    if table_bool == True:
        colors = []
        for i, color in enumerate(colors_list):
            row_color = [colors_list[i], 'white']
            colors.append(row_color)
            
        table = ax.table(cellText=table_df.values, cellLoc='center', colLabels=['Format', 'Songs Released'],
                  cellColours=colors, bbox=(1, 0.35, 0.5, 0.3))
        for (row, col), cell in table.get_celld().items():
            cell.set_text_props(fontproperties=FontProperties(size='large'))
            if (row == 0):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))
                
    if save_png == True:
        plt.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')

    return fig, ax

def release_hist(custom_params, df, x1_values, x2_values, x3_values, suptitle, title1, title2, title3, 
                 x1_label, x2_label, x3_label, y_label, colors_list, edgecolors_list, save_png=False, png_name=None):
    """Build three release histograms based on given arguments.

       Args:
           custom_params: dict, matplotlib custom params
           df: pandas dataframe
           x1_values: str, column name in df for first subplot
           x2_values: str, column name in df for second subplot
           x3_values: str, column name in df for third subplot
           suptitle: str, overall chart title
           title1: str, title for first subplot
           title2: str, title for second subplot
           title3: str, title for third subplot
           x1_label: str, x-axis label for first subplot
           x2_label: str, x-axis label for first subplot
           x3_label: str, x-axis label for first subplot
           y_label: str, y-axis label
           colors_list: list, colors for three histograms
           edgecolors_list: list, edgecolors for three histograms
           save_png: bool, default False, saves chart to png
           png_name: str, default None, image name (must include .png)
    """
    sns.set_theme(style='white', rc=custom_params)
    fig, ax = plt.subplots(1, 3, figsize=(16, 6), sharey=True)
    fig.patch.set_facecolor('#EDECE8')
    fig.suptitle(suptitle, fontweight='bold', fontsize='x-large')
    sns.histplot(df, x=x1_values, discrete=True, color=colors_list[0], edgecolor=edgecolors_list[0], alpha = 1, ax=ax[0], shrink=.8)
    first_ticks = [one for one in range(min(df[x1_values]), max(df[x1_values])+1, 3)]
    ax[0].set_xticks(first_ticks)
    ax[0].set_title(title1, fontweight='bold', fontsize='medium')
    ax[0].set_xlabel(x1_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    ax[0].set_ylabel(y_label, fontweight='bold', fontsize='medium')
    for c in ax[0].containers:
        ax[0].bar_label(c, fontweight='bold', fontsize=6)
    
    sns.histplot(df, x=x2_values, discrete=True, color=colors_list[1], edgecolor=edgecolors_list[0], alpha = 1, ax=ax[1], shrink=.8)
    second_ticks = [two for two in range(min(df[x2_values]), max(df[x2_values])+1, 3)]
    ax[1].set_xticks(second_ticks)
    ax[1].set_title(title2, fontweight='bold', fontsize='medium')
    ax[1].set_xlabel(x2_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    for c in ax[1].containers:
        ax[1].bar_label(c, fontweight='bold', fontsize=6)
    
    sns.histplot(df, x=x3_values, discrete=True, color=colors_list[2], edgecolor=edgecolors_list[0], alpha = 1, ax=ax[2], shrink=.8)
    third_ticks = [three for three in range(min(df[x3_values]), max(df[x3_values])+1, 3)]
    ax[2].set_xticks(third_ticks)
    ax[2].set_title(title3, fontweight='bold', fontsize='medium')
    ax[2].set_xlabel(x3_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    for c in ax[2].containers:
        ax[2].bar_label(c, fontweight='bold', fontsize=6)
    
    if save_png == True:
        plt.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')

    return fig, ax

def date_scatter(custom_params, df, x_values, y_values, size_values, title, x_label, 
                 y_label, save_png=False, png_name=None, table_bool=False, table_df=None):
    """Build collaborator heatmap based on given arguments.

       Args:
           custom_params: dict, matplotlib custom params
           df: pandas dataframe
           x_values: str, column name in df
           y_values: str, column name in df
           size_values: str, column name in df
           title: str, chart title
           x_label: str, x-axis label
           y_label: str, y-axis label
           save_png: bool, default False, saves chart to png
           png_name: str, default None, image name (must include .png)
           table_bool: bool, default False, includes values table
           table_df: formatted df, default None, needed for table 
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('#EDECE8')
    sns.scatterplot(df, x=x_values, y=y_values, size=size_values, hue=size_values, 
                    palette='autumn_r', edgecolor='#0d1b2a', marker='h', legend=False)
    sns.set_theme(style='white', rc=custom_params)
    sns.set(font_scale = 0.8)
    ax.set_title(title, fontweight='bold', fontsize='large', x=0.75)
    ax.set_xlabel(x_label, fontweight='bold', fontsize='medium',
           labelpad=5.5)
    ax.set_ylabel(y_label, fontweight='bold', fontsize='medium', 
               labelpad=5.5)
    if table_bool == True:
        ax.text(15.6, 28, 'Top 10', fontweight='bold', fontsize='medium')
        table = ax.table(cellText=table_df.values, cellLoc='center',
                         colLabels=['Date', 'Songs Released'], bbox=(1.1, 0.15, 0.4, 0.7))
        
        for (row, col), cell in table.get_celld().items():
            if (row == 0):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))
            if (row % 2 == 0):
                cell.set_color('#FEB23F')
                cell.set_edgecolor('#A03704')
            else:
                cell.set_edgecolor('#A03704')
        
    if save_png == True:
        plt.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')

    return fig, ax

def views_plots(custom_params, bar_df, barx_values, bary_values, hist_df, histx_values, suptitle, title1, title2,
                 x1_label, x2_label, y1_label, y2_label, colors_list, edgecolors_list, save_png=False, png_name=None):
    """Build three release histograms based on given arguments.

       Args:
           custom_params: dict, matplotlib custom params
           bar_df: pandas dataframe for barplot
           barx_value: str, column name in df for barplot
           bary_values: str, column name in df for barplot
           hist_df: pandas dataframe for histplot
           histx_value: str, column name in df for histplot
           suptitle: str, overall chart title
           title1: str, title for first subplot
           title2: str, title for second subplot
           x1_label: str, x-axis label for barplot
           x2_label: str, x-axis label for histplot
           y1_label: str, y-axis label for barplot
           y2_label: str, y-axis label for histplot
           colors_list: list, colors for two subplots
           edgecolors_list: list, edgecolors for two subplots
           save_png: bool, default False, saves chart to png
           png_name: str, default None, image name (must include .png)
    """
    sns.set_theme(style='white', rc=custom_params)
    fig, ax = plt.subplots(1, 2, figsize=(17, 6), gridspec_kw={'width_ratios': [1.5, 1]})
    fig.patch.set_facecolor('#EDECE8')
    fig.suptitle(suptitle, fontweight='bold', fontsize='x-large')
    sns.barplot(bar_df, y=bary_values, x=barx_values, errorbar=None, ax=ax[0], color=colors_list[0], edgecolor=edgecolors_list[0])
    ax[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.0f}M'.format(x/1000000)))
    for c in ax[0].containers:
        labels0 = ['{:.2f}M'.format(x/1000000) for x in c.datavalues] 
        ax[0].bar_label(c, labels=labels0, fontweight='bold', fontsize=8, padding= 2, label_type='edge')
    ax[0].set_title(title1, fontweight='bold', fontsize='medium')
    ax[0].set_xlabel(x1_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    ax[0].set_ylabel(y1_label, fontweight='bold', fontsize='medium')
    ax[0].margins(x=0.1)
    
    sns.histplot(hist_df, x=histx_values, ax=ax[1], color=colors_list[1], edgecolor=edgecolors_list[1], shrink=0.8)
    ax[1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.0f}M'.format(x/1000000)))
    for c in ax[1].containers:
        labels1 = [v if v > 0 else '' for v in c.datavalues] 
        ax[1].bar_label(c, labels=labels1, fontweight='bold', fontsize=6)
    ax[1].set_title(title2, fontweight='bold', fontsize='medium')
    ax[1].set_xlabel(x2_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    ax[1].set_ylabel(y2_label, fontweight='bold', fontsize='medium')
    
    if save_png == True:
        plt.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')

    return fig, ax

def views_box(custom_params, df, x_values, y_values, title, x_label, y_label, boxcolor, linecolor, save_png=False, png_name=None):
    """Build three release histograms based on given arguments.

       Args:
           custom_params: dict, matplotlib custom params
           df: pandas dataframe
           x_values: str, column name in df
           y_values: str, column name in df
           title: str, chart title
           x_label: str, x-axis label
           y_label: str, y-axis label
           boxcolor: str, color for box faces
           linecolor: str, color for lines
           save_png: bool, default False, saves chart to png
           png_name: str, default None, image name (must include .png)
    """
    sns.set_theme(style='white', rc=custom_params)
    fig, ax = plt.subplots(figsize=(17, 7))
    fig.patch.set_facecolor('#EDECE8')
    sns.boxplot(df, y=y_values, x=x_values, linecolor=linecolor, showmeans=True, 
                boxprops= {'facecolor': boxcolor}, flierprops={'marker': 'd', 'markerfacecolor': linecolor, 'markersize': 3},
                meanprops={'marker':'8', 'markerfacecolor': fig.get_facecolor(), 'markeredgecolor': linecolor})
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.0f}M'.format(x/1000000)))
    ax.set_title(title, fontweight='bold', fontsize='medium')
    ax.set_xlabel(x_label, fontweight='bold', fontsize='medium',
               labelpad=5.5)
    ax.set_ylabel(y_label, fontweight='bold', fontsize='medium')
    
    if save_png == True:
        plt.savefig('figures/charts/{}'.format(png_name), bbox_inches='tight')

    return fig, ax