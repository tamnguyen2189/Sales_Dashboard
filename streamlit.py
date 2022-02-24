from typing import OrderedDict
from altair.vegalite.v4.schema.core import Sort
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
# import seaborn as sns
# import matplotlib.pyplot as plt

# frame_a = pd.read_csv('C:/Users/pc/Desktop/my_git/presso/data/Sale_Q1_2021_(6).csv')
# frame_b= pd.read_csv('C:/Users/pc/Desktop/my_git/presso/data/Sale_Q2_2021.csv')
# df = frame.copy()
# 'Sale_2020.csv'

# How to concat multi csv file to dataframe:
# list_data = ['Sale_Q1_2021.csv','Sale_Q2_2021.csv']
# data_path = []
# for i in list_data:
#     dt_path = path + i
#     data_path.append(dt_path)
# frame_2021 = []
# for j in data_path:
#     frame_x = pd.read_csv(j)
#     frame_2021.append(frame_x)
# df_2021 = pd.concat(frame_2021,axis=0, ignore_index=True)


# Prepare the path to load dataset
path = 'C:/Users/pc/Desktop/my_git/Sales_Dashboard/data/'
data_path_2020 = path + 'Sale_2020.csv'
data_path_2021 = path + 'Sale_2021.csv'

# Read the dataset
frame_2020 = pd.read_csv(data_path_2020)
frame_2021 = pd.read_csv(data_path_2021)

df_2020 = frame_2020
df_2021 = frame_2021


# Beginning of Sales Dashboard
st.title('Sales Dashboard')
st.write('Summary')
year = st.selectbox('Select year', [2021,2020])
# Sales summary by year:
if year == 2020: 
    # Sum of revenue group by Date & Product:
    df_revenue = df_2020.groupby(['month','product_name'])[['total_cost','revenue','profit','quantity']].sum().reset_index()
    # Sum of revenue group by Date (all products)
    df_revenue_monthly = df_revenue.groupby('month')[['revenue','profit','quantity']].sum().reset_index()
if year == 2021:
    # Sum of revenue group by Date & Product:
    df_revenue = df_2021.groupby(['month','product_name'])[['total_cost','revenue','profit','quantity']].sum().reset_index()
    # Sum of revenue group by Date (all products)
    df_revenue_monthly = df_revenue.groupby('month')[['revenue','profit','quantity']].sum().reset_index()
# Chart of  sales_summary:
chart = alt.Chart(df_revenue_monthly).mark_bar(size = 15, color='#96ceb4').encode(# column='product_name',
                                                        x= alt.X('month',sort=None),
                                                        y='profit'
                                                        ).properties(width=600) 
st.write(chart)

# Sales by Drink Category :
st.write('Sales by Drink Category')
drink = st.multiselect('Please select:', [i for i in df_revenue['product_name'].unique()])
if len(drink) != 0:
    df_drink = df_revenue[df_revenue['product_name']==drink[0]]
    df_drink
    df_melt = df_drink.melt(id_vars=['month'], value_vars=['total_cost','revenue','profit'])
# Chart of Sales by Drink
    chart = alt.Chart(df_melt).mark_bar(size=10).encode(column='variable',
                                                    x=alt.X('month',sort=None,axis=alt.Axis(tickMinStep=1)),
                                                    y='sum(value)',
                                                    color='month')
    st.write(chart)

# Sales by Time period:
st.write('Sales by Time period')

opt = st.multiselect('Please select Year:', [2020, 2021])
year_list = [2021, 2020]
if len(opt) != 0:
    if opt[0] == 2020:
        df_revenue = df_2020.groupby(['month','product_name'])[['total_cost','revenue','profit','quantity']].sum().reset_index()
        df_revenue
    if opt[0] == 2021:
        df_revenue = df_2021.groupby(['month','product_name'])[['total_cost','revenue','profit','quantity']].sum().reset_index()
        df_revenue
        
    # month = st.selectbox('Select month', [f'{i}-{opt[0]}' for i in range(1,13)])
    month = st.selectbox('Select month', [i for i in range(1,13)])
    if month != 0:
        #Sum of monthly sales:
        st.text('Monthly Sales')
        df_revenue_monthly = df_revenue.groupby('month')[['revenue','profit','quantity']].sum().reset_index()
        sum_revenue = df_revenue_monthly[df_revenue_monthly['month']==month].sum()
        sum_revenue

        # Detail of monthly sales:
        st.text('Detail of Monthly Sales')
        sort_revenue = df_revenue[df_revenue['month']==month].sort_values(['profit'], ascending=False)
        sort_revenue

        # Chart of monthly sales:
        df_month = df_revenue #.groupby(['date','product_name'])[['total_cost','revenue','profit']].sum().reset_index()
        df_month_value = df_month[df_month['month']==month].sort_values(['profit'], ascending=False).head(10)
        df_melt = df_month_value.melt(id_vars=['product_name'], value_vars=['total_cost','revenue','profit'])
        
        all_value= alt.Chart(df_melt).mark_bar().encode(x=alt.X('product_name', sort='-y'),
                                                        y='sum(value)', 
                                                        color='variable').properties(height=500, width=800)                                    
        st.write(all_value)

        # Sort sales values:
        # chart= alt.Chart(sort_revenue).mark_bar().encode(x='profit',y=alt.Y('product_name',sort='-x'))                                              
        # st.write(chart)
        chart= alt.Chart(df_melt).mark_bar().encode(column = 'variable',
                                                    x='sum(value)',
                                                    y=alt.Y('product_name', sort='-x'),
                                                    color='variable').properties(height=400, width=250)                                               
        st.write(chart)



