import streamlit as st
import datetime

import pandas as pd 
import numpy as np
from glob import glob
import os
import time
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings("ignore")

import dthu
import cphi
import tkho
import kqkd
import kh

from helper import *

# https://api.github.com/repos/Huynh-Tr/report/contents/

# layout wide
# st.set_page_config(layout='wide')
# hide menu
st.markdown(
    """
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > header > div.stAppToolbar.st-emotion-cache-15ecox0.e4hpqof2 {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# center of the layout
st.markdown('<h1 style="text-align: center;">Dash Board</h1>', unsafe_allow_html=True)
st.divider()

st.header('Welcome to the dash board page!')
st.markdown(f'Today: {datetime.datetime.now().strftime('%d-%m-%Y')}')


st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 38px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')

start = time.time()

# divide to 5 columns
col1, col2, col3, col4, col5  = st.columns(5)

dthu_tsv, dthu_vm = dthu.dthu()

with st.sidebar.expander("Select year", expanded=False):
    year = [st.radio('Select year:', list(range(2025, 2023, -1)), index=0, label_visibility='collapsed')]

with st.sidebar.expander("Select month", expanded=False):
    month = [st.radio('Select month:', list(range(1, 13)), index=0, label_visibility='collapsed')]

with st.sidebar.expander("Select Plant Code", expanded=False):
    plant_code = [st.text_input('Select plant code:', 'Select All')]

with st.sidebar.expander("Select L2", expanded=False):
    L2 = [st.radio('Select L2:', ["All"] + dthu_tsv["Product Group 2 Name"].unique().tolist(), index=0, label_visibility='collapsed')]

with st.sidebar.expander("Select L3", expanded=False):
    L3 = [st.radio('Select L3:', ["All"] + dthu_tsv["Product Group 3 Name"].unique().tolist(), index=0, label_visibility='collapsed')]

with st.sidebar.expander("Select L4", expanded=False):
    L4 = [st.radio('Select L4:', ["All"] + dthu_tsv["Product Group 4 Name"].unique().tolist(), index=0, label_visibility='collapsed')]

# starttime

# Dthu plot
# st.write(dthu_tsv)
chitieu_th, chitieu_ck, chitieu_lk, chitieu_ck_lk = dthu.chitieu_theoky_plot(df=dthu_tsv, year=[2024, 2025], month=range(1, 13), plant_code='Select All')
def filter_df(df, L):    
    if L == ["All"]:
        return df
    return df[df["Product Group 2 Name"].isin(L)]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
df = filter_df(chitieu_th, L2)
df = filter_df(df, L3)
df = filter_df(df, L4)

# col1
df_dt_lg = (df.groupby(["Month year"])[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].sum().reset_index())
df_dt_lg["Month year"] = df_dt_lg["Month year"].dt.strftime('%Y-%m')
df_dt_lg.columns = ['Month year', 'Doanh Thu', 'Lãi Gộp']
fig1 = px.bar(df_dt_lg, x='Month year', y=['Doanh Thu', 'Lãi Gộp'], title='Doanh thu - Lãi gộp', labels={'value': 'Tỷ VND', 'variable': 'Loại'},
             barmode='group')
col1.plotly_chart(fig1, width=1400, height=400, use_container_width=False)

# col2
df_plant = (df.groupby(["Plant Code"])[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].sum()).sort_values(by='FM 01_Invoices Revenue', ascending=False).head(10)
df_plant.columns = ['Doanh Thu', 'Lãi Gộp']
fig2 = px.bar(df_plant, x=df_plant.index, y=['Doanh Thu', 'Lãi Gộp'], title='Doanh thu - Lãi gộp theo Plant', labels={'value': 'Tỷ VND', 'variable': 'Loại'},
             barmode='group')
fig2.update_layout(xaxis_type='category')
col2.plotly_chart(fig2)

#col3
df_dh = (df.groupby(["Product Group 4 Name"])[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].sum().reset_index().sort_values(by='FM 01_Invoices Revenue', ascending=False).head(10))
df_dh.columns = ['Product Group 4 Name', 'Doanh Thu', 'Lãi Gộp']
fig3 = px.bar(df_dh, x='Product Group 4 Name', y=['Doanh Thu', 'Lãi Gộp'], title='Doanh thu - Lãi gộp theo L4', labels={'value': 'Tỷ VND', 'variable': 'Loại'},
             barmode='group')
col3.plotly_chart(fig3, width=1400, height=400, use_container_width=False)

#col4
df_channel = (df.groupby(["Channel Description"])[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].sum().reset_index())
df_channel.columns = ['Channel', 'Doanh Thu', 'Lãi Gộp']
fig4 = px.bar(df_channel, x='Channel', y=['Doanh Thu', 'Lãi Gộp'], title='Doanh thu - Lãi gộp theo Channel', labels={'value': 'Tỷ VND', 'variable': 'Loại'},
             barmode='group')
col4.plotly_chart(fig4, width=1400, height=400, use_container_width=False)

# endtime
end = time.time()
# convert runtime
run_time = time.gmtime(end - start)
st.write("Run time: ", time.strftime("%M:%S", run_time))