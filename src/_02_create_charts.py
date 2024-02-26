import matplotlib.pyplot as plt
import pandas as pd

def stacked_bar_chart(bar_type, df, category_field, value_field, legend_field, color_dict, 
                      chart_title, x_label, y_label, subplot_pos, legend=False, legend_title=''):
    """Creates stacked bar chart in matplotlib.

       Args:
           bar_type: string, either 'bar' (vertical) or 'barh' (horizontal)
           df: dataframe (pandas)
           category_field: string, categorical df column name on either x- or y-axis
           value_field: string, quantitative df column name on either y- or x-axis 
               (opposite category_field)
           legend_field: string, categorical df column name that makes up 
               different bar segments
           color_dict: dictionary, {'legend_field': 'color'}
           chart_title: string, title of chart
           x_label: string, label on x-axis
           y_label: string, label on y-axis
           subplot_pos: axes object with subplot position, such as axes[0] or axes[1,0]
           legend: boolean, defaults to False, displays legend
           legend_title: string, defaults to empty, title for color legend
    """
    df_pivot = df.pivot_table(index=category_field, columns=legend_field, 
                              values=value_field, fill_value=0, aggfunc='sum')
    df_pivot.sort_values(category_field, ascending=False, inplace=True)
    
    df_chart = df_pivot.plot(kind=bar_type, figsize=(10, 10), width=0.7,
                             stacked=True, 
                             color=[color_dict[key] for key in df_pivot.keys()],
                             ax=subplot_pos, legend=legend)
    for container in df_chart.containers:
        r = container.patches[0].get_facecolor()[0]
        g = container.patches[0].get_facecolor()[1]
        b = container.patches[0].get_facecolor()[2]
    
        color = 'white' if r * g * b < 0.4 else 'black'
        
        if bar_type == 'barh':
            labels = [int(segment.get_width()) if segment.get_width() > 0 else '' for segment in container]
        elif bar_type =='bar':
            labels = [int(segment.get_height()) if segment.get_height() > 0 else '' for segment in container]
            
        df_chart.bar_label(container, labels=labels, label_type='center', color=color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(chart_title)
    
    if legend == True:
        plt.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')