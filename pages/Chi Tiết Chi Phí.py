import streamlit as st
import datetime
import yagmail

import pandas as pd 
import numpy as np
import os
import time

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

st.divider()

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

with st.sidebar.expander("Select year", expanded=False):
    year = [st.radio('Select year:', list(range(2025, 2023, -1)), index=0, label_visibility='collapsed')]

with st.sidebar.expander("Select month", expanded=False):
    month = [st.radio('Select month:', list(range(1, 13)), index=0, label_visibility='collapsed')]

with st.sidebar.expander("Select Plant Code", expanded=False):
    plant_code = [st.text_input('Select plant code:', 'Select All')]

parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/03h.parquet"

@st.cache_data
def glaccount():
    linkgl = r"D:\pnj.com.vn\HuynhTN - Documents\Dim\Dim_DanhMucTaiKhoan.xlsx"
    df = pd.read_excel(linkgl)
    df["G/L Account"] = df["G/L Account"].astype(str)
    return df

dimGL = glaccount()
# dimGL
df = pd.read_parquet(parquet)
df = df.merge(dimGL[["G/L Account", "Tên tài khoản"]], on="G/L Account", how="left")
df = df.drop(columns=["G/L Account", "Offsetting Account"])
cols = ["Cost Center", "Posting Date", "Tên tài khoản", "Description", "Amt", "Document Number", "Payment reference", "Asset"]
df = df[cols]
df = df[(df["Cost Center"].isin(plant_code)) & (df["Posting Date"].dt.year.isin(year)) & (df["Posting Date"].dt.month.isin(month))]

tab1, tab2 = st.tabs(2)
tab1.write(f'Total: {df['Amt'].sum():,.0f}')

tab1.write(df)