import pandas as pd
import streamlit as st 


path_gl = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/Dim_DanhMucTaiKhoan.XLSX'
@st.cache_data
def glaccount():
    df = pd.read_excel(path_gl)
    df["G/L Account"] = df["G/L Account"].astype(str)
    return df

path_ch = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/Dim_DanhSach_CH.xlsx'
@st.cache_data
def ten_ch():
    df = pd.read_excel(path_ch, sheet_name="CuaHang (4cum)", header=2)
    df["mã ch"] = df["mã ch"].astype(str)
    df["Ma-Ten"] = "[" + df["mã ch"] + " ] " + df["TÊN CỬA HÀNG"]
    return df

path_dsql = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/dims/dsql.xlsx'
@st.cache_data
def dsql():
    df = pd.read_excel(path_dsql)
    df['user'] = df['Email'].str.split('@').str[0]
    df['pwd'] = [str(i) for i in range(len(df))]
    return df