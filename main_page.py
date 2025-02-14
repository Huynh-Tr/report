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

    
# button clear cache
if st.button('Clear cache'):
    st.cache_data.clear()


data_tsv, data_vm = dthu.dthu()

def chitieu(year, month=1, plant_code='Select All'):    
    data_tsv, data_vm = dthu.dthu()
    if plant_code == 'Select All':
        sum_fm_tsv01 = data_tsv[(data_tsv["Month year"].dt.month.isin(month)) & (data_tsv["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
        sum_fm_vm01 = data_vm[(data_tsv["Month year"].dt.month.isin(month)) & (data_vm["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
        sum_fm_tsv07 = data_tsv[(data_tsv["Month year"].dt.month.isin(month)) & (data_tsv["Month year"].dt.year.isin(year))]["FM 07_Gross Profit"].sum() / 1e9
        sum_fm_vm07 = data_vm[(data_tsv["Month year"].dt.month.isin(month)) & (data_vm["Month year"].dt.year.isin(year))]["FM 07_Gross Profit"].sum() / 1e9
    else:
        sum_fm_tsv01 = data_tsv[(data_tsv["Plant Code"].isin(plant_code)) & (data_tsv["Month year"].dt.month.isin(month)) & (data_tsv["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
        sum_fm_vm01 = data_vm[(data_vm["Plant Code"].isin(plant_code)) & (data_tsv["Month year"].dt.month.isin(month)) & (data_vm["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
        sum_fm_tsv07 = data_tsv[(data_tsv["Plant Code"].isin(plant_code)) & (data_tsv["Month year"].dt.month.isin(month)) & (data_tsv["Month year"].dt.year.isin(year))]["FM 07_Gross Profit"].sum() / 1e9
        sum_fm_vm07 = data_vm[(data_vm["Plant Code"].isin(plant_code)) & (data_tsv["Month year"].dt.month.isin(month)) & (data_vm["Month year"].dt.year.isin(year))]["FM 07_Gross Profit"].sum() / 1e9

    return sum_fm_tsv01, sum_fm_vm01, sum_fm_tsv07, sum_fm_vm07     

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
# plant_code = [1277, 1617]
plant_code = data_tsv["Plant Code"].unique().tolist()

# add select all to the list
plant_code = ['Select All'] + plant_code
plant_code = col1.multiselect('Select plant code:', plant_code, default='Select All')

# multi selection year
# year = list(range(2021, 2026))
year = data_tsv["Month year"].dt.year.unique().tolist()
year = col2.multiselect('Select year:', year, default=year[-1])

# multi selection month
# month = list(range(1, 13))
month = data_tsv["Month year"].dt.month.unique().tolist()
month = col3.multiselect('Select month:', month)

st.write(plant_code, year, month)

if plant_code == ['Select All']:
    # chi tieu dthu lg
    sum_fm_tsv01 = data_tsv[(data_tsv["Month year"].dt.month.isin(month)) & (data_tsv["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
    st.write(sum_fm_tsv01)
# #     # chi tieu dthu lg
    sum_fm_tsv01, sum_fm_vm01, sum_fm_tsv07, sum_fm_vm07  = dthu.chitieu(year=[2025], month=1, plant_code='Select All')
    st.write(sum_fm_tsv01, sum_fm_vm01, sum_fm_tsv07, sum_fm_vm07)
#     # chi tieu cphi
#     # sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl = cphi.chitieu(year, month, plant_code)

# else:
#     # chi tieu dthu lg
#     sum_fm_tsv01, sum_fm_vm01, sum_fm_tsv07, sum_fm_vm07  = dthu.chitieu(year, month, plant_code)
    # chi tieu cphi
    # sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl = cphi.chitieu(year, month, plant_code)

# result_dthu = pd.DataFrame(
#     {
#         'Chỉ Tiêu': ['Doanh thu', 'TSV', 'VM', 'Lãi Gộp', 'TSV', 'VM'],
#         '': ['', '', '', '', '', ''],
#         'Thực Hiện': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
#         'Cùng Kỳ': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
#         'Kế Hoạch': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
#         ' ': ['', '', '', '', '', ''],
#         'LK Thực Hiện': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
#         'LK Cùng Kỳ': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
#         'LK Kế Hoạch': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
#         '  ': ['', '', '', '', '', ''],
#         'LK Thực Hiện ': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)],
#         'KH Năm': [round(sum_fm_tsv01 + sum_fm_vm01), round(sum_fm_tsv01), round(sum_fm_vm01), round(sum_fm_tsv07 + sum_fm_vm07), round(sum_fm_tsv07), round(sum_fm_vm07)]
#     }
# )

# # dataframe cphi
# result_cphi = pd.DataFrame(
#     {
#         "Chỉ Tiêu": ["Chi Phí Vận Hành", "Chi Phí Nhân Viên", "", "Chi Phí Ngoài Lương", 'CP CCDC', 'CP KH TSCĐ', 'CP vật liệu phụ',
#        'CP Còn lại', 'CP Thuê ngoài', 'CP hành chính', 'CP chuyển tiền', 'CP Marketing & Khuyến mãi', 'CP sửa chữa, bảo trì'],
#         '': ['' for i in range(13)],
#         # 'Thực Hiện': []
#         ' ': ['' for i in range(13)],
#         '  ': ['' for i in range(13)],
#     }
# )

# # Define lambda function to bold rows where the index is 1 or 3
# bold_rows_dthu = lambda x: ['font-weight: bold' if x.name in [0, 3] else '' for _ in x]
# bold_rows_cphi = lambda x: ['font-style: italic' if x.name in list(range(4, 13)) else '' for _ in x]

# # Apply the styling function
# styled_df_dthu = result_dthu.style.apply(bold_rows_dthu, axis=1)
# styled_df_cphi = result_cphi.style.apply(bold_rows_cphi, axis=1)

# # Apply 2 decimal places format to the DataFrame with text not formatted, set the number to right side
# styled_df_dthu = styled_df_dthu.format("{:.2f}", subset=pd.IndexSlice[:, ['Thực Hiện', 'Cùng Kỳ', 'Kế Hoạch', \
#                                                                 'LK Thực Hiện', 'LK Cùng Kỳ', 'LK Kế Hoạch', \
#                                                                 'LK Thực Hiện', 'LK Thực Hiện ', 'KH Năm']]) \
#                     .set_properties(**{'text-align': 'right'})

# # Display the styled DataFrame
# st.write(styled_df_dthu.to_html(), unsafe_allow_html=True)
# st.write(styled_df_cphi.to_html(), unsafe_allow_html=True)


# endtime
end = time.time()
# convert runtime
run_time = time.gmtime(end - start)
st.write("Run time: ", time.strftime("%M:%S", run_time))


