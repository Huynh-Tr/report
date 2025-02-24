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
st.markdown('<h1 style="text-align: center;">✌Main Page✌</h1>', unsafe_allow_html=True)

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

parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/03h.parquet"

df = pd.read_parquet(parquet)

st.write(df)