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


df = cphi.cphi()

st.write(df)