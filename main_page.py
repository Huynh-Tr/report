import streamlit as st
import datetime

import pandas as pd 
import numpy as np
from glob import glob
import os
import time

import warnings
warnings.filterwarnings("ignore")

import dthu
from helper import *

# layout wide
st.set_page_config(layout='wide')

# center of the layout
st.markdown('<h1 style="text-align: center;">Main Page</h1>', unsafe_allow_html=True)
st.divider()

st.header('Welcome to the main page!')
st.subheader(f'Today: {datetime.datetime.now().strftime('%d-%m-%Y')}')

# starttime
start = time.time()

# load data
data_tsv, data_vm = dthu.dthu()

st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 38px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')

# divide to 5 columns
col1, col2, col3, col4, col5 = st.columns(5)

# multi selection plant code
plant_code = data_tsv["Plant Code"].unique()
# add select all to the list
plant_code = ['Select All'] + plant_code.tolist()
plant_code = col1.multiselect('Select plant code:', plant_code, default='Select All')

# multi selection year
year = pd.to_datetime(data_tsv["Month year"]).dt.year.unique()
year = col3.multiselect('Select year:', year, default=year[-1])

# # multi selection month year
# month_year = data_tsv["Month year"].unique()
# month_year = col2.multiselect('Select month year:', month_year, default=month_year)

if plant_code == ['Select All']:
    sum_fm_tsv01 = data_tsv[data_tsv["Month year"].str.contains('|'.join(map(str, year)))]["FM 01_Invoices Revenue"].sum() / 1e9
    st.write(f'Doanh Thu TSV: {sum_fm_tsv01:.2f} tỉ')

    sum_fm_vm01 = data_vm[data_vm["Month year"].str.contains('|'.join(map(str, year)))]["FM 01_Invoices Revenue"].sum() / 1e9
    st.write(f'Doanh Thu VM: {sum_fm_vm01:.2f} tỉ')

    # sum of FM 07_Gross Profit
    sum_fm_tsv07 = data_tsv[data_tsv["Month year"].str.contains('|'.join(map(str, year)))]["FM 07_Gross Profit"].sum() / 1e9
    st.write(f'Lãi Gộp: {sum_fm_tsv07:.2f} tỉ')

    sum_fm_vm07 = data_vm[data_vm["Month year"].str.contains('|'.join(map(str, year)))]["FM 07_Gross Profit"].sum() / 1e9
    st.write(f'Lãi Gộp: {sum_fm_vm07:.2f} tỉ')
else:
    # sum of FM 01_Invoices Revenue
    sum_fm_tsv01 = data_tsv[data_tsv["Plant Code"].isin(plant_code) & data_tsv["Month year"].str.contains('|'.join(map(str, year)))]["FM 01_Invoices Revenue"].sum() / 1e9
    st.write(f'Doanh Thu TSV: {sum_fm_tsv01:.2f} tỉ')

    sum_fm_vm01 = data_vm[data_vm["Plant Code"].isin(plant_code) & data_vm["Month year"].str.contains('|'.join(map(str, year)))]["FM 01_Invoices Revenue"].sum() / 1e9
    st.write(f'Doanh Thu VM: {sum_fm_vm01:.2f} tỉ')


    # sum of FM 07_Gross Profit
    sum_fm_tsv07 = data_tsv[data_tsv["Plant Code"].isin(plant_code) & data_tsv["Month year"].str.contains('|'.join(map(str, year)))]["FM 07_Gross Profit"].sum() / 1e9
    st.write(f'Lãi Gộp TSV: {sum_fm_tsv07:.2f} tỉ')

    sum_fm_vm07 = data_vm[data_vm["Plant Code"].isin(plant_code) & data_vm["Month year"].str.contains('|'.join(map(str, year)))]["FM 07_Gross Profit"].sum() / 1e9
    st.write(f'Lãi Gộp VM: {sum_fm_vm07:.2f} tỉ')

result = pd.DataFrame(
    {
        'Chỉ Tiêu': ['Doanh thu', 'TSV', 'VM', 'Lãi Gộp', 'TSV', 'VM'],
        '': ['', '', '', '', '', ''],
        'Thực Hiện': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
        'Cùng Kỳ': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
        'Kế Hoạch': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
        ' ': ['', '', '', '', '', ''],
        'LK Thực Hiện': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
        'LK Cùng Kỳ': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
        'LK Kế Hoạch': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
        '  ': ['', '', '', '', '', ''],
        'LK Thực Hiện ': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
        'KH Năm': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)]
    }
)

# Function to bold rows 1 and 3
def bold_rows(row):
    if row.name in [0, 3]:  # Python indexing starts from 0
        return ['font-weight: bold'] * len(row)
    return [''] * len(row)

# Apply the styling function
styled_df = result.style.apply(bold_rows, axis=1)

# how to hide index


# Apply 2 decimal places format to the DataFrame with text not formatted, set the number to right side
styled_df = styled_df.format("{:.2f}", subset=pd.IndexSlice[:, ['Thực Hiện', 'Cùng Kỳ', 'Kế Hoạch', \
                                                                'LK Thực Hiện', 'LK Cùng Kỳ', 'LK Kế Hoạch', \
                                                                'LK Thực Hiện', 'LK Thực Hiện ', 'KH Năm']]) \
                    .set_properties(**{'text-align': 'right'})

# Display the styled DataFrame
st.write(styled_df.to_html(), unsafe_allow_html=True)

# endtime
end = time.time()
# convert runtime
run_time = time.gmtime(end - start)
st.write("Run time: ", time.strftime("%M:%S", run_time))


