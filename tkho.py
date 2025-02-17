import pandas as pd 
from glob import glob
import os
import requests
import streamlit as st
import helper

import warnings
warnings.filterwarnings("ignore")

parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/tonkho.parquet"

def tkho():
    df = pd.read_parquet(parquet)
    df = df[df["Month year"] != "Month year"]
    df["Month year"] = pd.to_datetime(df["Month year"]).dt.to_period('M')
    df["Plant Code"] = df["Plant Code"].astype('str')
    lv2 = ["DÂY ĐỒNG HỒ", "MẮT KÍNH", "ĐỒNG HỒ"]
    lv3 = ["CAO"]
    lv4 = ["TRANH/TƯỢNG/BIỂU TƯỢNG", "VÀNG ÉP SIÊU PNJ", "VÀNG ÉP SIÊU SJC"]
    cols = ["Month year", "Plant Code", "Product Group 2 Name", "Product Group 3 Name", "Product Group 4 Name", \
        "MM. Inventory Qty", "MM. Inventory Amt (Adjust)", "MM.Avg Inventory Qty", "MM.Avg Inventory Amt (Adjust)", \
        "FM 10_Inventory Cost", "MM. Repurchasing Amt", "MM. Repurchasing Qty"]

    df_tk_tsv = df.copy()
    df_tk_tsv = df_tk_tsv[~df_tk_tsv["Product Group 2 Name"].isin(lv2)]
    df_tk_tsv = df_tk_tsv[~df_tk_tsv["Product Group 3 Name"].isin(lv3)]
    df_tk_tsv = df_tk_tsv[~df_tk_tsv["Product Group 4 Name"].isin(lv4)]
    df_tk_tsv = df_tk_tsv[cols]

    df_tk_vm = df.copy()
    df_tk_vm = df_tk_vm[df_tk_vm["Product Group 4 Name"].isin(lv4)]
    df_tk_vm = df_tk_vm[cols]

    return df_tk_tsv, df_tk_vm

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
    df_tk_tsv, df_tk_vm = tkho()
    if plant_code == 'Select All':
        # chi phi von
        sum_cpv_tsv, sum_cpv_tsv_ck, sum_cpv_tsv_lk, sum_cpv_tsv_ck_lk = chitieu_theoky(df=df_tk_tsv, col="FM 10_Inventory Cost", year=year, month=month, plant_code=plant_code)
        sum_cpv_vm, sum_cpv_vm_ck, sum_cpv_vm_lk, sum_cpv_vm_ck_lk = chitieu_theoky(df=df_tk_vm, col="FM 10_Inventory Cost", year=year, month=month, plant_code=plant_code)
        # ton von
        sum_tv_tsv, sum_tv_tsv_ck, sum_tv_tsv_lk, sum_tv_tsv_ck_lk = chitieu_theoky(df=df_tk_tsv, col="MM.Avg Inventory Amt (Adjust)", year=year, month=month, plant_code=plant_code)
        sum_tv_vm, sum_tv_vm_ck, sum_tv_vm_lk, sum_tv_vm_ck_lk = chitieu_theoky(df=df_tk_vm, col="MM.Avg Inventory Amt (Adjust)", year=year, month=month, plant_code=plant_code)

    else:
        # chi phi von
        sum_cpv_tsv, sum_cpv_tsv_ck, sum_cpv_tsv_lk, sum_cpv_tsv_ck_lk = chitieu_theoky(df=df_tk_tsv, col="FM 10_Inventory Cost", year=year, month=month, plant_code=plant_code)
        sum_cpv_vm, sum_cpv_vm_ck, sum_cpv_vm_lk, sum_cpv_vm_ck_lk = chitieu_theoky(df=df_tk_vm, col="FM 10_Inventory Cost", year=year, month=month, plant_code=plant_code)
        # ton von
        sum_tv_tsv, sum_tv_tsv_ck, sum_tv_tsv_lk, sum_tv_tsv_ck_lk = chitieu_theoky(df=df_tk_tsv, col="MM.Avg Inventory Amt (Adjust)", year=year, month=month, plant_code=plant_code)
        sum_tv_vm, sum_tv_vm_ck, sum_tv_vm_lk, sum_tv_vm_ck_lk = chitieu_theoky(df=df_tk_vm, col="MM.Avg Inventory Amt (Adjust)", year=year, month=month, plant_code=plant_code)

    result_tkho = pd.DataFrame(
        {
        'Chỉ Tiêu': ['Chi Phí Vốn', 'TSV', 'VM'],
        '': ['', '', ''],
        '  Thực Hiện  ': [sum_cpv_tsv + sum_cpv_vm, sum_cpv_tsv, sum_cpv_vm],
        '  Cùng Kỳ    ': [sum_cpv_tsv_ck + sum_cpv_vm_ck, sum_cpv_tsv_ck, sum_cpv_vm_ck],
        '  Kế Hoạch   ': [sum_cpv_tsv + sum_cpv_vm, sum_cpv_tsv, sum_cpv_vm],
        ' ': ['', '', ''],
        ' LK Thực Hiện': [sum_cpv_tsv_lk + sum_cpv_vm_lk, sum_cpv_tsv_lk, sum_cpv_vm_lk],
        ' LK Cùng Kỳ  ': [sum_cpv_tsv_ck_lk + sum_cpv_vm_ck_lk, sum_cpv_tsv_ck_lk, sum_cpv_vm_ck_lk],
        ' LK Kế Hoạch ': [sum_cpv_tsv + sum_cpv_vm, sum_cpv_tsv, sum_cpv_vm],
        '  ': ['', '', ''],
        'LK Thực Hiện ': [sum_cpv_tsv_lk + sum_cpv_vm_lk, sum_cpv_tsv_lk, sum_cpv_vm_lk],
        '       KH Năm': [sum_cpv_tsv + sum_cpv_vm, sum_cpv_tsv, sum_cpv_vm]
        }
    )

    return result_tkho