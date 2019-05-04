# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 11:00:56 2018

@author: Suresh
"""
from calendar import month_abbr
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Panel, Tabs, Slider
from bokeh.layouts import layout, row
from bokeh.palettes import Spectral6
from bokeh.io import curdoc
from bokeh.plotting import figure


def tab_slider(e_df):
    e_df['month'] = e_df['month'].apply(lambda x: month_abbr[x])
    e_df['dayname'] = e_df.InvoiceDate.dt.weekday_name
    
    
    def cds_year1(mem,r=0):
        name = mem[r]
    #    print('in cds year1',name)
        year1 = e_df[e_df['month'] == name]['dayname'].value_counts()
        source = ColumnDataSource(name=name,data=dict(x=year1.index.values, y=year1.values, color=Spectral6))
        return source 
       
    def cds_year2(mem,r=0):
        name = mem[r]
    #    print('in cds year2',name)
        year1 = e_df[e_df['month'] == name]['dayname'].value_counts()
        source = ColumnDataSource(name=name,data=dict(x=year1.index.values, y=year1.values, color=Spectral6))
        return source    
    
    
    def plot_fig(source,name):
        p = figure(x_range=source.data['x'], y_range=(0,source.data['y'].max()+50), plot_height=600,
                   plot_width=1000, title=source.name,toolbar_location=None,
                   name=name,x_axis_label="Day of week",y_axis_label="Count")
        p.vbar(x='x', top='y', width=0.7, color='color',source=source)
        p.yaxis.minor_tick_line_color = None
        hover = HoverTool(tooltips=[('Month', source.name),("Count", "@y")])
        p.add_tools(hover)
        return p
    
    def change_child(source,name):
        sub_name = name.split('_')[0]
        root_list = curdoc().get_model_by_name(name)
        sublayout = root_list.children
        img_to_remove = curdoc().get_model_by_name(sub_name)
        sublayout.remove(img_to_remove)
        p = plot_fig(source,sub_name)
        sublayout.append(p)
    
    def slider1_callback(attr,old,new):
        f = slider1.value
        source1 = cds_year1(year1_slider,f) 
        change_child(source1,'year1_slider_layout')
        
    def slider2_callback(attr,old,new):
        f = slider2.value
        source2 = cds_year2(year2_slider,f)    
        change_child(source2,'year2_slider_layout')
        
        
    year1_slider = {}
    for i,j in enumerate(e_df[e_df['year'] == 2010]['month'].unique()):
        year1_slider[i] = j
        
    year2_slider = {}
    for i,j in enumerate(e_df[e_df['year'] == 2011]['month'].unique()):
        year2_slider[i] = j
        
    source1 = cds_year1(year1_slider)
    source2 = cds_year2(year2_slider)
    p1 = plot_fig(source1,'year1')
    p2 = plot_fig(source2,'year2')
    
    
    slider1 = Slider(start=0, end=len(year1_slider)-1, value=0, step=1, title='Month')
    slider2 = Slider(start=0, end=len(year2_slider)-1, value=0, step=1, title='Month')
    
    slider1.on_change('value',slider1_callback)
    slider2.on_change('value',slider2_callback)
    
    c1 = row(slider1,p1,name='year1_slider_layout')
    c2 = row(slider2,p2,name='year2_slider_layout')
    
    slider_layout1 = layout([[c1]],sizing_mode='scale_width')
    slider_layout2 = layout([[c2]])
    
    tab1 = Panel(child=slider_layout1, title="2010")
    tab2 = Panel(child=slider_layout2, title="2011")
    tabs = Tabs(tabs=[ tab1, tab2 ])
    return tabs

    

