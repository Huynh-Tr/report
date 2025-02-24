import pandas as pd
import streamlit as st 


path_gl = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/Dim_DanhMucTaiKhoan.xlsx'
@st.cache_data
def glaccount():
    df = pd.read_excel(path_gl)
    df["G/L Account"] = df["G/L Account"].astype(str)
    return df

path_ch = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/Dim_DanhSach_CH.xlsx'
@st.cache_data
def ten_ch():
    df = pd.read_excel(path_ch, sheet_name="CuaHang (4cum)", header=2)
    df = df[["mã ch", "TÊN CỬA HÀNG", "AREA"]]
    # create new column Ma-Ten = mã ch - TÊN CỬA HÀNG
    df["Ma-Ten"] = "[" + df["mã ch"].astype('str') + " ] " + df["TÊN CỬA HÀNG"]
    return df