import pandas as pd
import streamlit as st 

path_ch = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/Dim_DanhSach_CH.xlsx'
path_gl = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/Dim_DanhMucTaiKhoan.xlsx'

@st.cache_data
def glaccount(path_gl):
    df = pd.read_excel(linkgl)
    df["G/L Account"] = df["G/L Account"].astype(str)
    return df

@st.cache_data
def ten_ch(path_ch):
    df = pd.read_excel(linkch, sheet_name="CuaHang (4cum)", header=2)
    df = df[["mã ch", "TÊN CỬA HÀNG", "AREA"]]
    # create new column Ma-Ten = mã ch - TÊN CỬA HÀNG
    df["Ma-Ten"] = "[" + df["mã ch"].astype('str') + " ] " + df["TÊN CỬA HÀNG"]
    return df