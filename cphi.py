import pandas as pd 
from glob import glob
import os
import requests

import warnings
warnings.filterwarnings("ignore")

# def load_github_files():
#     url = 'https://api.github.com/repos/Huynh-Tr/report/contents/CP'
#     response = requests.get(url)
#     if response.status_code == 200:
#         files = pd.DataFrame(response.json())
#         files['name'] = files['name'].str.replace('.csv', '')
#         return files['download_url'].tolist()
#     else:
#         st.error("Failed to load data from GitHub.")
#         return None

parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/cphi.parquet"

def cphi():        
    df = pd.read_parquet(parquet)
    df["Month year"] = pd.to_datetime(df["Month year"]).dt.to_period('M')

    # create MaCH column with condition right 4 chartacters of cost center code if not null else right 4 characters of GL Account Code
    df["MaCH"] = df["Cost Center Code"].fillna(df["Plant Code"].astype('str')).astype('int').astype('str').str[-4:] \
        .replace('0000', 'P015').replace('9999', 'P015')

    df["FM. Loc Amt"] = df["FM. Loc Amt"].astype('float')

    cols = ["Month year", "GL Account Code", "GL LV1 Name", "FM. Loc Amt", "PnL Name", "MaCH"]
    gl_code_exl = 64110120 # list of GL Account Code
    gl_code_range = [64100000, 64252100]

    # filter data cols with gl_code_exl and in range gl_code_range
    df = df[cols][(df["GL Account Code"] != gl_code_exl) & (df["GL Account Code"].between(gl_code_range[0], gl_code_range[1]))]

    return df

def chitieu(year, month=1, plant_code='Select All'):
    data_cp = cphi()
    if plant_code == 'Select All':
        # sum of cphi
        sum_fm_cp = data_cp[data_cp["Month year"].dt.year.isin(year)]["FM. Loc Amt"].sum() / 1e9

        # cphi nhan vien
        sum_fm_cp_nv = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP Nhân viên"))]["FM. Loc Amt"].sum() / 1e9

        # cphi CCDC
        sum_fm_cp_ccdc = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP CCDC"))]["FM. Loc Amt"].sum() / 1e9

        # cphi kh tscd
        sum_fm_cp_khtscd = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP KH TSCD"))]["FM. Loc Amt"].sum() / 1e9

        # cphi vat lieu phu
        sum_fm_cp_vlp = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP vật liệu phụ"))]["FM. Loc Amt"].sum() / 1e9

        # cphi con lai
        sum_fm_cp_cl = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP Còn lại"))]["FM. Loc Amt"].sum() / 1e9

        # cphi thue ngoai
        sum_fm_cp_tn = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP Thuê ngoài"))]["FM. Loc Amt"].sum() / 1e9

        # cphi hanh chinh
        sum_fm_cp_hc = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP hành chính"))]["FM. Loc Amt"].sum() / 1e9

        # cphi chuyen tien
        sum_fm_cp_ct = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP chuyển tiền"))]["FM. Loc Amt"].sum() / 1e9

        # cphi marketing & khuyen mai
        sum_fm_cp_mk = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP Marketing & Khuyến mãi"))]["FM. Loc Amt"].sum() / 1e9

        # cphi sua chua, bao tri
        sum_fm_cp_scbt = data_cp[(data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP sửa chữa, bảo trì"))]["FM. Loc Amt"].sum() / 1e9
    
        # sum of cphi ngoai luong
        sum_fm_cp_nl = sum_fm_cp - sum_fm_cp_nv
    else:
            # sum of cphi
        sum_fm_cp = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year))]["FM. Loc Amt"].sum() / 1e9

        # cphi nhan vien
        sum_fm_cp_nv = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP Nhân viên"))]["FM. Loc Amt"].sum() / 1e9

        # cphi CCDC
        sum_fm_cp_ccdc = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP CCDC"))]["FM. Loc Amt"].sum() / 1e9

        # cphi kh tscd
        sum_fm_cp_khtscd = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP KH TSCD"))]["FM. Loc Amt"].sum() / 1e9

        # cphi vat lieu phu
        sum_fm_cp_vlp = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP vật liệu phụ"))]["FM. Loc Amt"].sum() / 1e9

        # cphi con lai
        sum_fm_cp_cl = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP Còn lại"))]["FM. Loc Amt"].sum() / 1e9

        # cphi thue ngoai
        sum_fm_cp_tn = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP Thuê ngoài"))]["FM. Loc Amt"].sum() / 1e9

        # cphi hanh chinh
        sum_fm_cp_hc = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP hành chính"))]["FM. Loc Amt"].sum() / 1e9

        # cphi chuyen tien
        sum_fm_cp_ct = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP chuyển tiền"))]["FM. Loc Amt"].sum() / 1e9

        # cphi marketing & khuyen mai
        sum_fm_cp_mk = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP Marketing & Khuyến mãi"))]["FM. Loc Amt"].sum() / 1e9

        # cphi sua chua, bao tri
        sum_fm_cp_scbt = data_cp[(data_tsv["Plant Code"].isin(plant_code)) & (data_cp["Month year"].dt.year.isin(year)) & (data_cp["GL LV1 Name"].str.contains("CP sửa chữa, bảo trì"))]["FM. Loc Amt"].sum() / 1e9
    
        # sum of cphi ngoai luong
        sum_fm_cp_nl = sum_fm_cp - sum_fm_cp_nv / 1e9

    return sum_fm_cp, sum_fm_cp_nv, sum_fm_cp_ccdc, sum_fm_cp_khtscd, sum_fm_cp_vlp, sum_fm_cp_cl, sum_fm_cp_tn, sum_fm_cp_hc, sum_fm_cp_ct, sum_fm_cp_mk, sum_fm_cp_scbt, sum_fm_cp_nl