import pandas as pd 
from glob import glob
import os
import requests
import streamlit as st
import helper

import warnings
warnings.filterwarnings("ignore")

parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/input/dthu.parquet"

@st.cache_data
def dthu():
    df = pd.read_parquet(parquet)
    df = df[df["Month year"] != "Month year"]
    df["Month year"] = pd.to_datetime(df["Month year"]).dt.to_period('M')
    df["Plant Code"] = df["Plant Code"].astype('str')
    # replace any text start with "Trang Sức Ý *" with "Trang Sức Ý" in column Product Group 4 Name
    df["Product Group 4 Name"] = df["Product Group 4 Name"].str.replace(r"^TRANG SỨC Ý.*", "TRANG SỨC Ý", regex=True)
    df["Product Group 4 Name"] = df["Product Group 4 Name"].str.replace("TRANG SỨC", "TS")
    lv2 = ["DÂY ĐỒNG HỒ", "MẮT KÍNH", "ĐỒNG HỒ"]
    lv3 = ["CAO"]
    lv4 = ["TRANH/TƯỢNG/BIỂU TƯỢNG", "VÀNG KHÔNG ÉP SIÊU", "VÀNG ÉP SIÊU PNJ", "VÀNG ÉP SIÊU SJC"]
    account_code = [51131000, 51132000]
    col = ["Product Group 2 Name", "Product Group 3 Name", "Product Group 4 Name", "Month year", \
        "Plant Code", "Channel Description", "FM 01_Invoices Revenue", "FM 07_Gross Profit"]

    df_tsv = df.copy()
    df_tsv = df_tsv[~df_tsv["Product Group 2 Name"].isin(lv2)]
    df_tsv = df_tsv[~df_tsv["Product Group 3 Name"].isin(lv3)]
    df_tsv = df_tsv[~df_tsv["Product Group 4 Name"].isin(lv4)]
    df_tsv = df_tsv[~df_tsv["GL Account Code"].isin(account_code)]
    df_tsv = df_tsv[col]

    df_vm = df.copy()
    df_vm = df_vm[df_vm["Product Group 4 Name"].isin(lv4)]
    df_vm = df_vm[col]

    return df_tsv, df_vm

def chitieu_theoky(df, col, year, month, plant_code):
    if plant_code == 'Select All':
        chitieu_th = df[(df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin(year))][col].sum() / 1e9
        chitieu_ck = df[(df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin([max(year) - 1]))][col].sum() / 1e9
        chitieu_lk = df[(df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin(year))][col].sum() / 1e9
        chitieu_ck_lk = df[(df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin([max(year) - 1]))][col].sum() / 1e9
    else:
        chitieu_th = df[(df["Plant Code"].isin(plant_code)) & (df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin(year))][col].sum() / 1e9
        chitieu_ck = df[(df["Plant Code"].isin(plant_code)) & (df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin([max(year) - 1]))][col].sum() / 1e9
        chitieu_lk = df[(df["Plant Code"].isin(plant_code)) & (df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin(year))][col].sum() / 1e9
        chitieu_ck_lk = df[(df["Plant Code"].isin(plant_code)) & (df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin([max(year) - 1]))][col].sum() / 1e9

    return chitieu_th, chitieu_ck, chitieu_lk, chitieu_ck_lk

def chitieu(year, month, plant_code='Select All'):    
    data_tsv, data_vm = dthu()
    # if plant_code == 'Select All':
    #     sum_fm_tsv01, sum_fm_tsv01_ck, sum_fm_tsv01_lk, sum_fm_tsv01_ck_lk = chitieu_theoky(df=data_tsv, col="FM 01_Invoices Revenue", year=year, month=month, plant_code=plant_code)
    #     sum_fm_vm01, sum_fm_vm01_ck, sum_fm_vm01_lk, sum_fm_vm01_ck_lk = chitieu_theoky(df=data_vm, col="FM 01_Invoices Revenue", year=year, month=month, plant_code=plant_code)                  
    #     sum_fm_tsv07, sum_fm_tsv07_ck, sum_fm_tsv07_lk, sum_fm_tsv07_ck_lk = chitieu_theoky(df=data_tsv, col="FM 07_Gross Profit", year=year, month=month, plant_code=plant_code)
    #     sum_fm_vm07, sum_fm_vm07_ck, sum_fm_vm07_lk, sum_fm_vm07_ck_lk = chitieu_theoky(df=data_vm, col="FM 07_Gross Profit", year=year, month=month, plant_code=plant_code)

    # else:
    sum_fm_tsv01, sum_fm_tsv01_ck, sum_fm_tsv01_lk, sum_fm_tsv01_ck_lk = chitieu_theoky(df=data_tsv, col="FM 01_Invoices Revenue", year=year, month=month, plant_code=plant_code)
    sum_fm_vm01, sum_fm_vm01_ck, sum_fm_vm01_lk, sum_fm_vm01_ck_lk = chitieu_theoky(df=data_vm, col="FM 01_Invoices Revenue", year=year, month=month, plant_code=plant_code)                  
    sum_fm_tsv07, sum_fm_tsv07_ck, sum_fm_tsv07_lk, sum_fm_tsv07_ck_lk = chitieu_theoky(df=data_tsv, col="FM 07_Gross Profit", year=year, month=month, plant_code=plant_code)
    sum_fm_vm07, sum_fm_vm07_ck, sum_fm_vm07_lk, sum_fm_vm07_ck_lk = chitieu_theoky(df=data_vm, col="FM 07_Gross Profit", year=year, month=month, plant_code=plant_code)
    
    result_dthu = pd.DataFrame(
        {
        'Chỉ Tiêu': ['Doanh thu', '- TSV ', '- VM ', 'Lãi Gộp', '- TSV  ', '- VM  '],
        '': ['', '', '', '', '', ''],
        '  Thực Hiện  ': [(sum_fm_tsv01 + sum_fm_vm01), (sum_fm_tsv01), (sum_fm_vm01), (sum_fm_tsv07 + sum_fm_vm07), (sum_fm_tsv07), (sum_fm_vm07)],
        '  Cùng Kỳ    ': [(sum_fm_tsv01_ck + sum_fm_vm01_ck), (sum_fm_tsv01_ck), (sum_fm_vm01_ck), (sum_fm_tsv07_ck + sum_fm_vm07_ck), (sum_fm_tsv07_ck), (sum_fm_vm07_ck)],
        ' ': ['', '', '', '', '', ''],
        ' LK Thực Hiện': [(sum_fm_tsv01_lk + sum_fm_vm01_lk), (sum_fm_tsv01_lk), (sum_fm_vm01_lk), (sum_fm_tsv07_lk + sum_fm_vm07_lk), (sum_fm_tsv07_lk), (sum_fm_vm07_lk)],
        ' LK Cùng Kỳ  ': [(sum_fm_tsv01_ck_lk + sum_fm_vm01_ck_lk), (sum_fm_tsv01_ck_lk), (sum_fm_vm01_ck_lk), (sum_fm_tsv07_ck_lk + sum_fm_vm07_ck_lk), (sum_fm_tsv07_ck_lk), (sum_fm_vm07_ck_lk)],
        '  ': ['', '', '', '', '', ''],
        'LK Thực Hiện ': [(sum_fm_tsv01_lk + sum_fm_vm01_lk), (sum_fm_tsv01_lk), (sum_fm_vm01_lk), (sum_fm_tsv07_lk + sum_fm_vm07_lk), (sum_fm_tsv07_lk), (sum_fm_vm07_lk)],
        }
    )    

    return result_dthu                  

def chitieu_theoky_plot(df, year, month, plant_code='Select All'):
    if plant_code == 'Select All':
        chitieu_th = df[(df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin(year))]
        chitieu_ck = df[(df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin([max(year) - 1]))]
        chitieu_lk = df[(df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin(year))]
        chitieu_ck_lk = df[(df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin([max(year) - 1]))]
    else:
        chitieu_th = df[(df["Plant Code"].isin(plant_code)) & (df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin(year))]
        chitieu_ck = df[(df["Plant Code"].isin(plant_code)) & (df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin([max(year) - 1]))]
        chitieu_lk = df[(df["Plant Code"].isin(plant_code)) & (df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin(year))]
        chitieu_ck_lk = df[(df["Plant Code"].isin(plant_code)) & (df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin([max(year) - 1]))]

    return chitieu_th, chitieu_ck, chitieu_lk, chitieu_ck_lk