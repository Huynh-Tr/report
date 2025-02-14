import pandas as pd 
from glob import glob
import os
import requests
import streamlit as st

import warnings
warnings.filterwarnings("ignore")

parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/dthu.parquet"

def dthu():
    df = pd.read_parquet(parquet)
    df = df[df["Month year"] != "Month year"]
    df["Month year"] = pd.to_datetime(df["Month year"]).dt.to_period('M')
    lv2 = ["DÂY ĐỒNG HỒ", "MẮT KÍNH", "ĐỒNG HỒ"]
    lv3 = ["CAO"]
    lv4 = ["TRANH/TƯỢNG/BIỂU TƯỢNG", "VÀNG ÉP SIÊU PNJ", "VÀNG ÉP SIÊU SJC"]
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

def chitieu(year, month=1, plant_code='Select All'):    
    data_tsv, data_vm = dthu()
    if plant_code == 'Select All':
        sum_fm_tsv01 = data_tsv[(data_tsv["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
        sum_fm_vm01 = data_vm[(data_tsv["Month year"].dt.month.isin(month)) & (data_vm["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
        sum_fm_tsv07 = data_tsv[(data_tsv["Month year"].dt.month.isin(month)) & (data_tsv["Month year"].dt.year.isin(year))]["FM 07_Gross Profit"].sum() / 1e9
        sum_fm_vm07 = data_vm[(data_tsv["Month year"].dt.month.isin(month)) & (data_vm["Month year"].dt.year.isin(year))]["FM 07_Gross Profit"].sum() / 1e9
    else:
        sum_fm_tsv01 = data_tsv[(data_tsv["Plant Code"].isin(plant_code)) & (data_tsv["Month year"].dt.month.isin(month)) & (data_tsv["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
        sum_fm_vm01 = data_vm[(data_vm["Plant Code"].isin(plant_code)) & (data_tsv["Month year"].dt.month.isin(month)) & (data_vm["Month year"].dt.year.isin(year))]["FM 01_Invoices Revenue"].sum() / 1e9
        sum_fm_tsv07 = data_tsv[(data_tsv["Plant Code"].isin(plant_code)) & (data_tsv["Month year"].dt.month.isin(month)) & (data_tsv["Month year"].dt.year.isin(year))]["FM 07_Gross Profit"].sum() / 1e9
        sum_fm_vm07 = data_vm[(data_vm["Plant Code"].isin(plant_code)) & (data_tsv["Month year"].dt.month.isin(month)) & (data_vm["Month year"].dt.year.isin(year))]["FM 07_Gross Profit"].sum() / 1e9

    return sum_fm_tsv01, sum_fm_vm01, sum_fm_tsv07, sum_fm_vm07     