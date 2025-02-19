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
st.subheader(f'Today: {datetime.datetime.now().strftime('%d-%m-%Y')}')


st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 38px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')

# divide to 5 columns
col1, col2, col3, col4, col5  = st.columns(5)

# multi selection plant code
plant_code = ['1277', '1617']
# plant_code = data_tsv["Plant Code"].unique().tolist()

# add select all to the list
plant_code = ['Select All'] + plant_code
plant_code = col1.multiselect('Select plant code:', plant_code, default=['Select All'])

# multi selection year
year = list(range(2021, 2026))
# year = data_tsv["Month year"].dt.year.unique().tolist()
year = col2.multiselect('Select year:', year, default=datetime.datetime.now().year)

# multi selection month
month = list(range(1, 13))
# month = data_tsv["Month year"].dt.month.unique().tolist()
month = col3.multiselect('Select month:', month, default=datetime.datetime.now().month)

# starttime
start = time.time()

# Dthu plot
dthu_tsv, dthu_vm = dthu.dthu()
# st.write(dthu_tsv)
chitieu_th, chitieu_ck, chitieu_lk, chitieu_ck_lk = dthu.chitieu_theoky_plot(df=dthu_tsv, year=[2024, 2025], month=range(1, 13), plant_code='Select All')
df = (chitieu_th.groupby(["Month year"])[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].sum() / 1e9 )
# st.write(df.values)


fig, ax = plt.subplots(2, 2, figsize=(20, 20))
# fig 1
df.plot(kind='bar', ax=ax[0, 0])
ax[0, 0].set_title('Doanh thu')
ax[0, 0].set_xlabel('Tháng')
ax[0, 0].set_ylim([0, 300])
ax[0, 0].set_ylabel('Tỷ VND')
ax[0, 0].legend(['Doanh Thu', 'Lãi Gộp'], loc='upper right')
# set no border
ax[0, 0].spines['top'].set_visible(False)
ax[0, 0].spines['right'].set_visible(False)
# st.pyplot(fig)

# fig 2
f2 = (chitieu_th.groupby(["Product Group 4 Name"])[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].sum() / 1e9).sort_values(by="FM 01_Invoices Revenue", ascending=False)[:10]
f2["%"] = f2["FM 07_Gross Profit"] / f2["FM 01_Invoices Revenue"]
ax2 = ax[0, 1].twinx()
f2[["FM 01_Invoices Revenue", "FM 07_Gross Profit"]].plot(kind='bar', color='blue', alpha=0.7, ax=ax[0, 1])
f2["%"].plot(kind='line', color='red', alpha=0.1, marker='*', secondary_y=True, ax=ax[0, 1])
for i, txt in enumerate(f2["%"]):
    ax2.annotate(f'{txt:.2%}', (i, f2["%"].iloc[i]), textcoords="offset points", xytext=(0.1,0.1), ha='center', color='red')

for item in ax[0, 1].get_xticklabels():
    item.set_rotation(90)

plt.tight_layout()
st.pyplot(fig)

# fig 3

# fig 4

# endtime
end = time.time()
# convert runtime
run_time = time.gmtime(end - start)
st.write("Run time: ", time.strftime("%M:%S", run_time))