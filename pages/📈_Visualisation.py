import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Visualisation", page_icon="📈", layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title('Data Visualization Facilitator')

df = pd.DataFrame()

if 'df' in st.session_state:
    df = st.session_state['df']
    cols = df.columns
    num_cols = [col for col in cols if pd.api.types.is_numeric_dtype(df[col])]

if 'charts' in st.session_state:
    charts = st.session_state['charts']
else:
    charts = []

def split_two_cols(x, y):
    col3, col4 = st.columns([1, 1])
    with col3:
        x_axis = st.selectbox(
            x, 
            [""] + list(cols))
    with col4:
        y_axis = st.selectbox(
            y,
            [""] + list(num_cols))
    return (x_axis, y_axis)

def add_chart(**kwargs):
    charts.append(kwargs["data"])

def line_charts():
    (x_axis, y_axis) = split_two_cols('x_axis', 'y_axis')
    
    if x_axis != "" and y_axis != "":
        title = st.text_input('Title', y_axis+" over "+ x_axis)
        res = df.groupby(x_axis)[y_axis].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=res.index, y=res.values))
        fig.update_layout(title= title, xaxis_title=x_axis,
        yaxis_title=y_axis)

        st.plotly_chart(fig, use_container_width=True)
        st.button("Add Chart", on_click=add_chart, kwargs={"data":fig})

def bar_charts():
    (x_axis, y_axis) = split_two_cols('x_axis', 'y_axis')

    if x_axis != "" and y_axis != "":
        title = st.text_input('Title', y_axis+" by "+ x_axis)
        res = df.groupby(x_axis)[y_axis].sum()
        fig = go.Figure([go.Bar(x=res.index, y=res.values, text=res.values, textposition='auto')])
        fig.update_layout(title=title, xaxis_title=x_axis,
        yaxis_title=y_axis)
        st.plotly_chart(fig, use_container_width=True)
        st.button("Add Chart", on_click=add_chart, kwargs={"data":fig})
    elif x_axis != "":
        res = df[x_axis].value_counts()
        fig = go.Figure([go.Bar(x=res.index, y=res.values, text=res.values, textposition='auto')])
        fig.update_layout(title=x_axis + ' counts', xaxis_title=x_axis, yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
        st.button("Add Chart", on_click=add_chart, kwargs={"data":fig})

def scatter_plots():
    (x_axis, y_axis) = split_two_cols('x_axis', 'y_axis')

    if x_axis != "" and y_axis != "":
        fig = go.Figure(data=go.Scatter(x=df[x_axis], y=df[y_axis], mode='markers'))
        fig.update_layout(title=y_axis+" vs. "+ x_axis, xaxis_title=x_axis,
        yaxis_title=y_axis)
        st.plotly_chart(fig, use_container_width=True)
        st.button("Add Chart", on_click=add_chart, kwargs={"data":fig})

# def bubble_charts():
#     (x_axis, y_axis) = split_two_cols('x_axis', 'y_axis')
#     size = st.selectbox(
#             'size', 
#             [""] + list(num_cols))
#     if x_axis != "" and y_axis != "":
#         if size == "":
#             size = None
#         else:
#             size = df[size]
#         fig = go.Figure(data=[go.Scatter(
#         x=df[x_axis], y=df[y_axis],
#         mode='markers',
#         marker_size=size)])
#         st.plotly_chart(fig, use_container_width=True)

def pie_charts():
    (labels, values) = split_two_cols('labels', 'values')
    if labels != "" and values != "":
        title = st.text_input('Title', values+" by "+labels)
        fig = go.Figure(data=[go.Pie(labels=df[labels], values=df[values])])
        fig.update_layout(title=title)
        st.plotly_chart(fig, use_container_width=True)
        st.button("Add Chart", on_click=add_chart, kwargs={"data":fig})

def box_plots():
    options = st.multiselect(
    '',
    num_cols)
    if len(options) > 0:
        fig = go.Figure()
        for op in options:
            fig.add_trace(go.Box(y=df[op]))
        fig.update_layout(title="Box plots of "+ str(options))
        st.plotly_chart(fig, use_container_width=True)
        st.button("Add Chart", on_click=add_chart, kwargs={"data":fig})

def hist():
    x_axis = st.selectbox("x_axis", [""] + list(cols))
    if x_axis != "":
        title = st.text_input('Title', "Histogram of "+ x_axis)
        bin_size = st.number_input('Bin size')
        fig = go.Figure(data=[go.Histogram(
            x=df[x_axis], 
            xbins=dict(size=bin_size)
            )])
        fig.update_layout(title=title)
        st.plotly_chart(fig, use_container_width=True)
        st.button("Add Chart", on_click=add_chart, kwargs={"data":fig})

col1, col2 = st.columns([1, 4])

with col1:
    selected = option_menu(None, ['Line Charts', 'Bar Charts', 'Scatter Plots', 'Pie Charts',# 'Bubble Charts', 
                                  'Box Plots', 'Histograms'], 
        icons=['graph-up', 'bar-chart-line', 'diagram-2-fill', 'pie-chart-fill',# 'dot', 
               'align-middle', 'reception-2'], 
        menu_icon="cast", default_index=0, orientation="vertical")

if len(df) > 0:
    with col2:
        match selected:
            case "Line Charts":
                line_charts()
            case "Bar Charts":
                bar_charts()
            case "Scatter Plots":
                scatter_plots()
            case "Pie Charts":
                pie_charts()
            # case "Bubble Charts":
            #     bubble_charts()
            case "Box Plots":
                box_plots()
            case "Histograms":
                hist()
            
st.session_state['charts'] = charts

