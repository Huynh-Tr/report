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
year = list(range(2021, 2026))
# year = data_tsv["Month year"].dt.year.unique().tolist()
year = col2.multiselect('Select year:', year, default=year[-1])

# multi selection month
month = list(range(1, 13))
# month = data_tsv["Month year"].dt.month.unique().tolist()
month = col3.multiselect('Select month:', month)

if plant_code == ['Select All']:
    # chi tieu dthu lg
    sum_fm_tsv01, sum_fm_vm01, sum_fm_tsv07, sum_fm_vm07  = dthu.chitieu(year=year, month=month, plant_code='Select All')
    # chi tieu cphi
    sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt, sum_fm_cp_nl = cphi.chitieu(year=year, month=month, plant_code='Select All')
else:
    # chi tieu dthu lg
    sum_fm_tsv01, sum_fm_vm01, sum_fm_tsv07, sum_fm_vm07  = dthu.chitieu(year=year, month=month, plant_code=plant_code)
    # chi tieu cphi
    sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt, sum_fm_cp_nl = cphi.chitieu(year=year, month=month, plant_code=plant_code)

result_dthu = pd.DataFrame(
    {
        'Chỉ Tiêu': ['Doanh thu', 'TSV', 'VM', 'Lãi Gộp', 'TSV', 'VM'],
        '': ['', '', '', '', '', ''],
        '  Thực Hiện  ': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)],
        '  Cùng Kỳ    ': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)],
        '  Kế Hoạch   ': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)],
        ' ': ['', '', '', '', '', ''],
        ' LK Thực Hiện': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)],
        ' LK Cùng Kỳ  ': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)],
        ' LK Kế Hoạch ': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)],
        '  ': ['', '', '', '', '', ''],
        'LK Thực Hiện ': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)],
        '       KH Năm': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)]
    }
)

# dataframe cphi
result_cphi = pd.DataFrame(
    {
        "Chỉ Tiêu": ["Chi Phí Vận Hành", "Chi Phí Nhân Viên", "Chi Phí Ngoài Lương", 'CP CCDC', 'CP KH TSCĐ', 'CP vật liệu phụ',
       'CP Còn lại', 'CP Thuê ngoài', 'CP hành chính', 'CP chuyển tiền', 'CP Marketing & Khuyến mãi', 'CP sửa chữa, bảo trì'],
        '': ['' for i in range(12)],
        '  Thực Hiện  ': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt],
        '  Cùng Kỳ    ': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt],
        '  Kế Hoạch   ': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt],
        ' ': ['' for i in range(12)],
        ' LK Thực Hiện': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt],
        ' LK Cùng Kỳ  ': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt],
        ' LK Kế Hoạch ': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt],
        '  ': ['' for i in range(12)],
        'LK Thực Hiện ': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt],
        '       KH Năm': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt]
    }
)

# Define lambda function to bold rows where the index is 1 or 3
bold_rows_dthu = lambda x: ['font-weight: bold' if x.name in [0, 3] else '' for _ in x]
bold_rows_cphi = lambda x: ['font-weight: bold' if x.name in [0] else '' for _ in x]
italic_rows_cphi = lambda x: ['font-style: italic' if x.name in list(range(4, 13)) else '' for _ in x]

# Apply the styling function
styled_df_dthu = result_dthu.style.apply(bold_rows_dthu, axis=1)
styled_df_cphi = result_cphi.style.apply(bold_rows_cphi, axis=1)

df = pd.concat([result_dthu, result_cphi], axis=0).reset_index(drop=True)

bold_rows_df = lambda x: ['font-weight: bold' if x.name in [0, 3, 6] else '' for _ in x]
italic_row_df = lambda x: ['font-style: italic' if x.name in list(range(9, 18)) else '' for _ in x]

# Apply the styling function to the DataFrame bold_rows_df and italic_row_df
styled_df = df.style.apply(bold_rows_df, axis=1).apply(italic_row_df, axis=1)

# Apply 2 decimal places format to the DataFrame with text formatted on the left side, set the number to right side, header to center
styled_df = styled_df.format("{:.2f}", subset=pd.IndexSlice[:, ['  Thực Hiện  ', '  Cùng Kỳ    ', '  Kế Hoạch   ', \
                                                                ' LK Thực Hiện', ' LK Cùng Kỳ  ', ' LK Kế Hoạch ', \
                                                                'LK Thực Hiện ', '       KH Năm']]) \
                    .set_properties(**{'text-align': 'right'}) \
                    .set_properties(subset=pd.IndexSlice[:, ['Chỉ Tiêu']], **{'text-align': 'left'}) \
                    .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])

# hide index of dataframe
styled_df = styled_df.hide(axis='index')

st.write(styled_df.to_html(), unsafe_allow_html=True)

# endtime
end = time.time()
# convert runtime
run_time = time.gmtime(end - start)
st.write("Run time: ", time.strftime("%M:%S", run_time))
