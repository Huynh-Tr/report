import pandas as pd 
from glob import glob
import os
import requests
import streamlit as st

import warnings
warnings.filterwarnings("ignore")

parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/cphi.parquet"

# @st.cache_data
def cphi():        
    df = pd.read_parquet(parquet)
    df["Month year"] = pd.to_datetime(df["Month year"]).dt.to_period('M')
    df = df[df["Company Code"] == 1000]
    # create MaCH column with condition right 4 chartacters of cost center code if not null else right 4 characters of GL Account Code
    df["MaCH"] = df["Cost Center Code"].fillna(df["Plant Code"].astype('str')).astype('str').str[-6:-2] \
        .replace('0000', 'P015').replace('9999', 'P015')
    
    df["FM. Loc Amt"] = df["FM. Loc Amt"].astype('float')

    cols = ["Month year", "GL Account Code", "GL LV1 Name", "FM. Loc Amt", "PnL Name", "MaCH"]
    gl_code_exl = 64110120 # list of GL Account Code
    gl_code_range = [64100000, 64252100]

    # filter data cols with gl_code_exl and in range gl_code_range
    df = df[cols][(df["GL Account Code"] != gl_code_exl) & (df["GL Account Code"].between(gl_code_range[0], gl_code_range[1]))]

    return df

def chitieu_theoky(df, col_cp, col, year, month, plant_code):
    if plant_code == 'Select All':
        chitieu_th = df[(df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin(year)) & (df["GL LV1 Name"].str.contains(col_cp))][col].sum() / 1e9 * -1
        chitieu_ck = df[(df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin([max(year) - 1])) & (df["GL LV1 Name"].str.contains(col_cp))][col].sum() / 1e9 * -1
        chitieu_lk = df[(df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin(year)) & (df["GL LV1 Name"].str.contains(col_cp))][col].sum() / 1e9 * -1
        chitieu_ck_lk = df[(df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin([max(year) - 1])) & (df["GL LV1 Name"].str.contains(col_cp))][col].sum() / 1e9 * -1

    else:
        chitieu_th = df[(df["MaCH"].isin(plant_code)) & (df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin(year)) & (df["GL LV1 Name"].str.contains(col_cp))][col].sum() / 1e9 * -1
        chitieu_ck = df[(df["MaCH"].isin(plant_code)) & (df["Month year"].dt.month.isin(month)) & (df["Month year"].dt.year.isin([max(year) - 1])) & (df["GL LV1 Name"].str.contains(col_cp))][col].sum() / 1e9 * -1
        chitieu_lk = df[(df["MaCH"].isin(plant_code)) & (df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin(year)) & (df["GL LV1 Name"].str.contains(col_cp))][col].sum() / 1e9 * -1
        chitieu_ck_lk = df[(df["MaCH"].isin(plant_code)) & (df["Month year"].dt.month.isin(range(1, max(month) + 1))) & (df["Month year"].dt.year.isin([max(year) - 1])) & (df["GL LV1 Name"].str.contains(col_cp))][col].sum() / 1e9 * -1

    return chitieu_th, chitieu_ck, chitieu_lk, chitieu_ck_lk

def chitieu(year, month=1, plant_code='Select All'):
    data_cp = cphi()
    # if plant_code == 'Select All':
    #     # cphi nhan vien
    #     sum_fm_cp_nv, sum_fm_cp_nv_ck, sum_fm_cp_nv_lk, sum_fm_cp_nv_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP Nhân viên", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    #     # cphi CCDC
    #     sum_fm_cp_ccdc, sum_fm_cp_ccdc_ck, sum_fm_cp_ccdc_lk, sum_fm_cp_ccdc_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP CCDC", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)
        
    #     # cphi kh tscd
    #     sum_fm_cp_khtscd, sum_fm_cp_khtscd_ck, sum_fm_cp_khtscd_lk, sum_fm_cp_khtscd_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP KH TSCĐ", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    #     # cphi vat lieu phu
    #     sum_fm_cp_vlp, sum_fm_cp_vlp_ck, sum_fm_cp_vlp_lk, sum_fm_cp_vlp_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP vật liệu phụ", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    #     # cphi con lai
    #     sum_fm_cp_cl, sum_fm_cp_cl_ck, sum_fm_cp_cl_lk, sum_fm_cp_cl_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP Còn lại", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    #     # cphi thue ngoai
    #     sum_fm_cp_tn, sum_fm_cp_tn_ck, sum_fm_cp_tn_lk, sum_fm_cp_tn_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP Thuê ngoài", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    #     # cphi hanh chinh
    #     sum_fm_cp_hc, sum_fm_cp_hc_ck, sum_fm_cp_hc_lk, sum_fm_cp_hc_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP hành chính", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    #     # cphi chuyen tien
    #     sum_fm_cp_ct, sum_fm_cp_ct_ck, sum_fm_cp_ct_lk, sum_fm_cp_ct_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP chuyển tiền", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    #     # cphi marketing & khuyen mai
    #     sum_fm_cp_mk, sum_fm_cp_mk_ck, sum_fm_cp_mk_lk, sum_fm_cp_mk_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP Marketing & Khuyến mãi", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    #     # cphi sua chua, bao tri
    #     sum_fm_cp_scbt, sum_fm_cp_scbt_ck, sum_fm_cp_scbt_lk, sum_fm_cp_scbt_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP sửa chữa, bảo trì", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)
    
    # else:
    # cphi nhan vien
    sum_fm_cp_nv, sum_fm_cp_nv_ck, sum_fm_cp_nv_lk, sum_fm_cp_nv_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP Nhân viên", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    # cphi CCDC
    sum_fm_cp_ccdc, sum_fm_cp_ccdc_ck, sum_fm_cp_ccdc_lk, sum_fm_cp_ccdc_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP CCDC", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)
    
    # cphi kh tscd
    sum_fm_cp_khtscd, sum_fm_cp_khtscd_ck, sum_fm_cp_khtscd_lk, sum_fm_cp_khtscd_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP KH TSCĐ", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    # cphi vat lieu phu
    sum_fm_cp_vlp, sum_fm_cp_vlp_ck, sum_fm_cp_vlp_lk, sum_fm_cp_vlp_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP vật liệu phụ", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    # cphi con lai
    sum_fm_cp_cl, sum_fm_cp_cl_ck, sum_fm_cp_cl_lk, sum_fm_cp_cl_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP Còn lại", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    # cphi thue ngoai
    sum_fm_cp_tn, sum_fm_cp_tn_ck, sum_fm_cp_tn_lk, sum_fm_cp_tn_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP Thuê ngoài", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    # cphi hanh chinh
    sum_fm_cp_hc, sum_fm_cp_hc_ck, sum_fm_cp_hc_lk, sum_fm_cp_hc_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP hành chính", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    # cphi chuyen tien
    sum_fm_cp_ct, sum_fm_cp_ct_ck, sum_fm_cp_ct_lk, sum_fm_cp_ct_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP chuyển tiền", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    # cphi marketing & khuyen mai
    sum_fm_cp_mk, sum_fm_cp_mk_ck, sum_fm_cp_mk_lk, sum_fm_cp_mk_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP Marketing & Khuyến mãi", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)

    # cphi sua chua, bao tri
    sum_fm_cp_scbt, sum_fm_cp_scbt_ck, sum_fm_cp_scbt_lk, sum_fm_cp_scbt_ck_lk = chitieu_theoky(df=data_cp, col_cp="CP sửa chữa, bảo trì", col="FM. Loc Amt", year=year, month=month, plant_code=plant_code)
    

    # sum of cphi ngoai luong
    sum_fm_cp_nl = sum_fm_cp_ccdc + sum_fm_cp_khtscd + sum_fm_cp_vlp + sum_fm_cp_cl + sum_fm_cp_tn + sum_fm_cp_hc + sum_fm_cp_ct + sum_fm_cp_mk + sum_fm_cp_scbt
    sum_fm_cp_nl_ck = sum_fm_cp_ccdc_ck + sum_fm_cp_khtscd_ck + sum_fm_cp_vlp_ck + sum_fm_cp_cl_ck + sum_fm_cp_tn_ck + sum_fm_cp_hc_ck + sum_fm_cp_ct_ck + sum_fm_cp_mk_ck + sum_fm_cp_scbt_ck
    sum_fm_cp_nl_lk = sum_fm_cp_ccdc_lk + sum_fm_cp_khtscd_lk + sum_fm_cp_vlp_lk + sum_fm_cp_cl_lk + sum_fm_cp_tn_lk + sum_fm_cp_hc_lk + sum_fm_cp_ct_lk + sum_fm_cp_mk_lk + sum_fm_cp_scbt_lk
    sum_fm_cp_nl_ck_lk = sum_fm_cp_ccdc_ck_lk + sum_fm_cp_khtscd_ck_lk + sum_fm_cp_vlp_ck_lk + sum_fm_cp_cl_ck_lk + sum_fm_cp_tn_ck_lk + sum_fm_cp_hc_ck_lk + sum_fm_cp_ct_ck_lk + sum_fm_cp_mk_ck_lk + sum_fm_cp_scbt_ck_lk

    # sum of cphi
    sum_fm_cp = sum_fm_cp_nv + sum_fm_cp_ccdc + sum_fm_cp_khtscd + sum_fm_cp_vlp + sum_fm_cp_cl + sum_fm_cp_tn + sum_fm_cp_hc + sum_fm_cp_ct + sum_fm_cp_mk + sum_fm_cp_scbt
    sum_fm_cp_ck = sum_fm_cp_nv_ck + sum_fm_cp_ccdc_ck + sum_fm_cp_khtscd_ck + sum_fm_cp_vlp_ck + sum_fm_cp_cl_ck + sum_fm_cp_tn_ck + sum_fm_cp_hc_ck + sum_fm_cp_ct_ck + sum_fm_cp_mk_ck + sum_fm_cp_scbt_ck
    sum_fm_cp_lk = sum_fm_cp_nv_lk + sum_fm_cp_ccdc_lk + sum_fm_cp_khtscd_lk + sum_fm_cp_vlp_lk + sum_fm_cp_cl_lk + sum_fm_cp_tn_lk + sum_fm_cp_hc_lk + sum_fm_cp_ct_lk + sum_fm_cp_mk_lk + sum_fm_cp_scbt_lk
    sum_fm_cp_ck_lk = sum_fm_cp_nv_ck_lk + sum_fm_cp_ccdc_ck_lk + sum_fm_cp_khtscd_ck_lk + sum_fm_cp_vlp_ck_lk + sum_fm_cp_cl_ck_lk + sum_fm_cp_tn_ck_lk + sum_fm_cp_hc_ck_lk + sum_fm_cp_ct_ck_lk + sum_fm_cp_mk_ck_lk + sum_fm_cp_scbt_ck_lk

    # dataframe cphi
    result_cphi = pd.DataFrame(
        {
            "Chỉ Tiêu": ["Chi Phí Vận Hành", "+ Chi Phí Nhân Viên", "+ Chi Phí Ngoài Lương", '- CP CCDC', '- CP KH TSCĐ', '- CP vật liệu phụ',
        '- CP Còn lại', '- CP Thuê ngoài', '- CP hành chính', '- CP chuyển tiền', '- CP Marketing & Khuyến mãi', '- CP sửa chữa, bảo trì'],
            '': ['' for i in range(12)],
            '  Thực Hiện  ': [sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_nl, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt],
            '  Cùng Kỳ    ': [sum_fm_cp_ck, sum_fm_cp_nv_ck, sum_fm_cp_nl_ck, sum_fm_cp_ccdc_ck, sum_fm_cp_khtscd_ck, sum_fm_cp_vlp_ck, sum_fm_cp_cl_ck, sum_fm_cp_tn_ck, sum_fm_cp_hc_ck, sum_fm_cp_ct_ck, sum_fm_cp_mk_ck, sum_fm_cp_scbt_ck],
            ' ': ['' for i in range(12)],
            ' LK Thực Hiện': [sum_fm_cp_lk, sum_fm_cp_nv_lk, sum_fm_cp_nl_lk, sum_fm_cp_ccdc_lk, sum_fm_cp_khtscd_lk, sum_fm_cp_vlp_lk, sum_fm_cp_cl_lk, sum_fm_cp_tn_lk, sum_fm_cp_hc_lk, sum_fm_cp_ct_lk, sum_fm_cp_mk_lk, sum_fm_cp_scbt_lk],
            ' LK Cùng Kỳ  ': [sum_fm_cp_ck_lk, sum_fm_cp_nv_ck_lk, sum_fm_cp_nl_ck_lk, sum_fm_cp_ccdc_ck_lk, sum_fm_cp_khtscd_ck_lk, sum_fm_cp_vlp_ck_lk, sum_fm_cp_cl_ck_lk, sum_fm_cp_tn_ck_lk, sum_fm_cp_hc_ck_lk, sum_fm_cp_ct_ck_lk, sum_fm_cp_mk_ck_lk, sum_fm_cp_scbt_ck_lk],
            '  ': ['' for i in range(12)],
            'LK Thực Hiện ': [sum_fm_cp_lk, sum_fm_cp_nv_lk, sum_fm_cp_nl_lk, sum_fm_cp_ccdc_lk, sum_fm_cp_khtscd_lk, sum_fm_cp_vlp_lk, sum_fm_cp_cl_lk, sum_fm_cp_tn_lk, sum_fm_cp_hc_lk, sum_fm_cp_ct_lk, sum_fm_cp_mk_lk, sum_fm_cp_scbt_lk],
        }
    )

    return result_cphi