import streamlit as st
import datetime
# import yagmail
import plotly.express as px

import pandas as pd 
import numpy as np
import os
import time

import dim

import warnings
warnings.filterwarnings("ignore")

from helper import *

# https://api.github.com/repos/Huynh-Tr/report/contents/

# layout wide
st.set_page_config(layout='wide')
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
st.markdown('<h1 style="text-align: center;">✔Chi tiết chi phí</h1>', unsafe_allow_html=True)

# st.divider()

# starttime
start = time.time()

# data_tsv, data_vm = dthu.dthu()

st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 38px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')

dimGL = dim.glaccount()
# filter 641
dimGL_filter = dimGL[(dimGL["G/L Account"].str.startswith('64'))][~dimGL["G/L Account"].str.startswith('6411')]

dimCH = dim.ten_ch()

# parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/03h.parquet"
parquet = r"D:\pnj.com.vn\HuynhTN - Documents\Project\streamlit\03h.parquet"

# dimGL
df = pd.read_parquet(parquet)
df = df.merge(dimCH, left_on="Cost Center", right_on="mã ch", how="left")
df = df.merge(dimGL, on="G/L Account", how="left")
df = df.drop(columns=["G/L Account", "Offsetting Account"])

# df
cols = ["Ma-Ten", "Posting Date", "Tên tài khoản", "Description", "Amt", "Document Number", "Asset", "Cost Center"]
df_details = df[cols]

with st.sidebar.expander("Select year", expanded=False):
    year = [st.radio('Select year:', list(range(2025, 2023, -1)), index=0, label_visibility='collapsed')]

with st.sidebar.expander("Select month", expanded=False):
    month = [st.radio('Select month:', list(range(1, 13)), index=0, label_visibility='collapsed')]

with st.sidebar.expander("Select Plant Code", expanded=False):
    plant_code = st.multiselect('Select GL Name:', df['Cost Center'].unique(), label_visibility='collapsed')

with st.sidebar.expander("Select GL Name", expanded=False):
    gl_name = st.multiselect('Select GL Name:', dimGL_filter['Tên tài khoản'].dropna().unique(), label_visibility='collapsed')

if plant_code == [] and gl_name == []:
    df = df[(df["Posting Date"].dt.year.isin(year)) & (df["Posting Date"].dt.month.isin(month))]
elif plant_code == []:
    df = df[(df["Posting Date"].dt.year.isin(year)) & (df["Posting Date"].dt.month.isin(month)) & (df["Tên tài khoản"].isin(gl_name))]
elif gl_name == []:
    df = df[(df["Cost Center"].isin(plant_code)) & (df["Posting Date"].dt.year.isin(year)) & (df["Posting Date"].dt.month.isin(month))]
else:
    df = df[(df["Cost Center"].isin(plant_code)) & (df["Posting Date"].dt.year.isin(year)) & (df["Posting Date"].dt.month.isin(month)) & (df["Tên tài khoản"].isin(gl_name))]

tab1, tab2 = st.tabs(["Chi tiết chi phí", "Tổng hợp chi phí"])
tab1.write(f'Total: {df_details['Amt'].sum():,.0f}')

tab1.data_editor(df_details, hide_index=True, height=500, width=1400)

# plot donut chart using plotly
fig = px.pie(df.groupby("Name")["Amt"].sum().reset_index(), values='Amt', names='Name', title='Tổng hợp chi phí')

col1, col2 = tab2.columns(2)

col1.plotly_chart(fig)