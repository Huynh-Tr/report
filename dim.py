import pandas as pd
import streamlit as st 


@st.cache_data
def glaccount():
    path_gl = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/Dim_DanhMucTaiKhoan.xlsx'
    df = pd.read_excel(path_gl)
    df["G/L Account"] = df["G/L Account"].astype(str)
    return df

@st.cache_data
def ten_ch():
    path_ch = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/Dim_DanhSach_CH.xlsx'
    df = pd.read_excel(path_ch, sheet_name="CuaHang (4cum)", header=2)
    df = df[["mã ch", "TÊN CỬA HÀNG", "AREA"]]
    # create new column Ma-Ten = mã ch - TÊN CỬA HÀNG
    df["Ma-Ten"] = "[" + df["mã ch"].astype('str') + " ] " + df["TÊN CỬA HÀNG"]
    return df