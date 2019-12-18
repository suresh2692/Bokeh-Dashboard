# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 11:05:23 2018

@author: Suresh
"""

from bokeh.core.properties import value
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import curdoc

from math import pi
import numpy as np
import pandas as pd
from tab_slider import tab_slider


def load_and_preprocess():
    df = pd.read_csv('./data/online_retail.zip', compression='zip', encoding='unicode_escape')
    df['InvoiceDate'] = pd.to_datetime(df.InvoiceDate)
    df['year'] = df.InvoiceDate.dt.year
    df['month'] = df.InvoiceDate.dt.month
    df['quarter'] = df.InvoiceDate.dt.quarter
    df['quarter'] = df['quarter'].map(lambda x: 'Q{}'.format(x))

    return df


# =============================================================================
# stacked chart
# =============================================================================

def stacked_bar(df):
    y_df = df.groupby(['quarter','year'])['quarter'].count()
    years = y_df.index.get_level_values('year').unique().values
    quarter = y_df.index.get_level_values('quarter').unique()
    colors = Category20c[len(quarter)]
    l = len(years)
    data = {'years':years}
    
    for r in quarter:
        data[r] = y_df[r].values
        t = l - len(data[r])
        if t!=0:
            data[r] = np.append(data[r], np.zeros(t))
        
    p = figure(x_range=years, plot_height=500,plot_width=1000, title="Year wise Sales",
           toolbar_location=None, tools="hover", tooltips="$name @years: @$name",
           x_axis_label="Year",y_axis_label="Sales")

    p.vbar_stack(quarter, x='years', width=0.9,color=colors, source=data,muted_alpha=0.1,
                 legend=[value(x) for x in quarter])
    
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "vertical"
    p.legend.click_policy="mute"
    return p


# =============================================================================
# Pie chart
# =============================================================================

def pie_chart(df):
    
    ccounts = df.Country.value_counts()
    df.loc[df['Country'].isin(ccounts[ccounts.values < 500].index),'Country'] = 'Others'
    
    rf = pd.DataFrame(df['Country'].value_counts())
    rf['angle'] = rf['Country']/rf['Country'].sum() * 2*pi
    rf['color'] = Category20c[rf.shape[0]]
    
    p = figure(plot_height=500, title="Country wise Sales", toolbar_location=None,
               tools="hover", tooltips="@index: @Country", x_range=(-0.5, 1.0))
    
    p.wedge(x=0, y=1, radius=0.5,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='index', source=rf)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    return p

# =============================================================================
# Multiple tabs with slider
# =============================================================================

e_df = load_and_preprocess()

stacked = stacked_bar(e_df)
pie = pie_chart(e_df)
tabbed = tab_slider(e_df)

tab1 = Panel(child=stacked, title="Year-wise")
tab2 = Panel(child=pie, title="Region-wise")
tab3 = Panel(child=tabbed, title="Monthly Drilldown")
tabs = Tabs(tabs=[ tab1, tab2, tab3])


curdoc().title = "Retail Sales"
curdoc().theme = 'light_minimal'
curdoc().add_root(tabs)
