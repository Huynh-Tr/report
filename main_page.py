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
import cphi
import tkho
import kqkd
import kh

from helper import *

# https://api.github.com/repos/Huynh-Tr/report/contents/

# layout wide
st.set_page_config(layout='wide')

# center of the layout
st.markdown('<h1 style="text-align: center;">Main Page</h1>', unsafe_allow_html=True)
st.divider()

st.header('Welcome to the main page!')
st.subheader(f'Today: {datetime.datetime.now().strftime('%d-%m-%Y')}')

# starttime
start = time.time()

    
# button clear cache
if st.button('Clear cache'):
    st.cache_data.clear()


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
plant_code = ['1277', '1617']
# plant_code = data_tsv["Plant Code"].unique().tolist()

# add select all to the list
plant_code = ['Select All'] + plant_code
plant_code = col1.multiselect('Select plant code:', plant_code)

# multi selection year
year = list(range(2021, 2026))
# year = data_tsv["Month year"].dt.year.unique().tolist()
year = col2.multiselect('Select year:', year, default=year[-1])

# multi selection month
month = list(range(1, 13))
# month = data_tsv["Month year"].dt.month.unique().tolist()
month = col3.multiselect('Select month:', month, default=month[-1])

if plant_code==['Select All']:
    # chi tieu dthu lg
    result_dthu  = dthu.chitieu(year=year, month=month, plant_code='Select All')
    # chi tieu cphi
    result_cphi = cphi.chitieu(year=year, month=month, plant_code='Select All')
    # chi tieu ton kho
    result_tkho = tkho.chitieu(year=year, month=month, plant_code='Select All')
    # ke hoach
    # result_kh = kh.result_kh(year=year, month=month, plant_code='Select All').set_index('Chỉ Tiêu')

else:
    # chi tieu dthu lg
    result_dthu  = dthu.chitieu(year=year, month=month, plant_code=plant_code)
    # chi tieu cphi
    result_cphi = cphi.chitieu(year=year, month=month, plant_code=plant_code)
    # chi tieu ton kho
    result_tkho = tkho.chitieu(year=year, month=month, plant_code=plant_code)
    # ke hoach
    # result_kh = kh.result_kh(year=year, month=month, plant_code=plant_code).set_index('Chỉ Tiêu')


# st.write('Result DThu:', result_dthu)
# st.write('Result CPhi:', result_cphi)
# st.write('Result TKho:', result_tkho)

def kqkd(result_dthu, result_tkho, result_cphi):
    kqkd_th = result_dthu.iloc[3, 2] + result_tkho.iloc[0, 2] + result_cphi.iloc[0, 2]
    kqkd_ck = result_dthu.iloc[3, 3] + result_tkho.iloc[0, 3] + result_cphi.iloc[0, 3]
    kqkd_lk = result_dthu.iloc[3, 6] + result_tkho.iloc[0, 6] + result_cphi.iloc[0, 6]
    kqkd_ck_lk = result_dthu.iloc[3, 6] + result_tkho.iloc[0, 6] + result_cphi.iloc[0, 6]

    kqkd_ex_vm_th = result_dthu.iloc[3, 2] + result_tkho.iloc[0, 2] + result_cphi.iloc[0, 2] - result_dthu.iloc[5, 2] - result_tkho.iloc[2, 3]
    kqkd_ex_vm_ck = result_dthu.iloc[3, 3] + result_tkho.iloc[0, 3] + result_cphi.iloc[0, 3] - result_dthu.iloc[5, 3] - result_tkho.iloc[2, 3]
    kqkd_ex_vm_lk = result_dthu.iloc[3, 6] + result_tkho.iloc[0, 6] + result_cphi.iloc[0, 6] - result_dthu.iloc[5, 6] - result_tkho.iloc[2, 6]
    kqkd_ex_vm_ck_lk = result_dthu.iloc[3, 6] + result_tkho.iloc[0, 6] + result_cphi.iloc[0, 6] - result_dthu.iloc[5, 6] - result_tkho.iloc[2, 6]

    result_kqkd = pd.DataFrame(
        {
            'Chỉ Tiêu': ['LNTT', 'LNTT(-VM)', 'LNST', 'LNST(-VM)'],
            '': ['', '', '', ''],
            '  Thực Hiện  ': [kqkd_th, kqkd_ex_vm_th, kqkd_th * 0.8, kqkd_ex_vm_th * 0.8],
            '  Cùng Kỳ    ': [kqkd_ck, kqkd_ex_vm_ck, kqkd_ck * 0.8, kqkd_ex_vm_ck * 0.8],
            ' ': ['', '', '', ''],
            ' LK Thực Hiện': [kqkd_lk, kqkd_ex_vm_lk, kqkd_lk * 0.8, kqkd_ex_vm_lk * 0.8],
            ' LK Cùng Kỳ  ': [kqkd_ck_lk, kqkd_ex_vm_ck_lk, kqkd_ck_lk * 0.8, kqkd_ex_vm_ck_lk * 0.8],
            '  ': ['', '', '', ''],
            'LK Thực Hiện ': [kqkd_lk, kqkd_ex_vm_lk, kqkd_lk * 0.8, kqkd_ex_vm_lk * 0.8],
        }
    )
    return result_kqkd

result_kqkd = kqkd(result_dthu, result_tkho, result_cphi)

# concat dataframes
df = pd.concat([result_dthu, result_cphi, result_tkho, result_kqkd], axis=0).set_index('Chỉ Tiêu')
# .reset_index(drop=True)
    # result_kqkd

# concat kh
# df = pd.concat([df, result_kh], axis=1)
# .reset_index(drop=True)
# df = df.merge(result_kh, left_index=True, right_index=True)
# st.write('Result DThu:', kh.get_chitieu(df, "Doanh Thu", "TSV", thang=month, nam=year, plant_code='Select All'))

# st.write(df)
st.write(kh.result_kh(year=year, month=month, plant_code='Select All'))

# bold_rows_df = lambda x: ['font-weight: bold' if x.name in [0, 3, 6, 18, 21, 22, 23, 24] else '' for _ in x]
# italic_row_df = lambda x: ['font-style: italic' if x.name in list(range(9, 18)) else '' for _ in x]

# # Apply the styling function to the DataFrame bold_rows_df and italic_row_df
# styled_df = df.style.apply(bold_rows_df, axis=1).apply(italic_row_df, axis=1)

# # Apply 2 decimal places format to the DataFrame with text formatted on the left side, set the number to right side, header to center
# styled_df = styled_df.format("{:.2f}", subset=pd.IndexSlice[:, ['  Thực Hiện  ', '  Cùng Kỳ    ', '  Kế Hoạch   ', \
#                                                                 ' LK Thực Hiện', ' LK Cùng Kỳ  ', ' LK Kế Hoạch ', \
#                                                                 'LK Thực Hiện ', '       KH Năm']]) \
#                     .set_properties(**{'text-align': 'right'}) \
#                     .set_properties(subset=pd.IndexSlice[:, ['Chỉ Tiêu']], **{'text-align': 'left'}) \
#                     .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])

# # hide index of dataframe
# styled_df = styled_df.hide(axis='index')

# st.write(styled_df.to_html(), unsafe_allow_html=True)

# endtime
end = time.time()
# convert runtime
run_time = time.gmtime(end - start)
st.write("Run time: ", time.strftime("%M:%S", run_time))
