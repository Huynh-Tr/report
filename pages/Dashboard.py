import streamlit as st
import datetime

import pandas as pd 
import numpy as np
from glob import glob
import os
import time
import matplotlib.pyplot as plt

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

df = filter_df(chitieu_th, L2)
df = filter_df(df, L3)
df = filter_df(df, L4)
df = (df.groupby(["Month year"])[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].sum() / 1e9 )

fig, ax = plt.subplots(2, 2, figsize=(20, 20))
# fig 1
df.plot(kind='bar', ax=ax[0, 0])
ax[0, 0].set_title('Doanh thu - Lãi gộp')
ax[0, 0].set_xlabel('Tháng')
# ax[0, 0].set_ylim([0, 300])
ax[0, 0].set_ylabel('Tỷ VND')
ax[0, 0].legend(['Doanh Thu', 'Lãi Gộp'], loc='upper right')
# set no border
ax[0, 0].spines['top'].set_visible(False)
ax[0, 0].spines['right'].set_visible(False)
st.pyplot(fig)

# fig 2
# f2 = (chitieu_th.groupby(["Product Group 4 Name"])[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].sum() / 1e9).sort_values(by="FM 01_Invoices Revenue", ascending=False)[:10]
# f2["%"] = f2["FM 07_Gross Profit"] / f2["FM 01_Invoices Revenue"]
# ax2 = ax[0, 1].twinx()
# f2[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].plot(kind='bar', color='blue', alpha=0.7, ax=ax[0, 1])
# f2["%"].plot(kind='line', color='red', alpha=0.1, marker='*', secondary_y=True, ax=ax[0, 1])
# for i, txt in enumerate(f2["%"]):
#     ax2.annotate(f'{txt:.2%}', (i, f2["%"].iloc[i]), textcoords="offset points", xytext=(0.1,0.1), ha='center', color='red')

# for item in ax[0, 1].get_xticklabels():
#     item.set_rotation(90)

# plt.tight_layout()
# st.pyplot(fig)

# fig 3
# df = cphi.cphi()

# st.write(df)
# fig 4

# endtime
end = time.time()
# convert runtime
run_time = time.gmtime(end - start)
st.write("Run time: ", time.strftime("%M:%S", run_time))