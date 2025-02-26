import pandas as pd
from glob import glob
import os
import requests
import warnings
import streamlit as st

warnings.filterwarnings("ignore")

path = r'https://raw.githubusercontent.com/Huynh-Tr/report/main/input/kh.parquet'

@st.cache_data
def kehoach():
    df = pd.read_parquet(path)
    return df

def get_chitieu(df, chi_phi, chi_tiet, thang, nam, plant_code='Select All'):
    if plant_code=='Select All':
        ky_nay = round(df[(df["Chi Phí"] == chi_phi) & (df["Chi tiết"] == chi_tiet) & (df["Tháng"].dt.month.isin(thang)) & (df["Tháng"].dt.year.isin(nam))]["Amt"].sum() / 1e3, 2)
        lk = round(df[(df["Chi Phí"] == chi_phi) & (df["Chi tiết"] == chi_tiet) & (df["Tháng"].dt.month.isin(range(1, max(thang) + 1))) & (df["Tháng"].dt.year.isin(nam))]["Amt"].sum() / 1e3, 2)
        ca_nam = round(df[(df["Chi Phí"] == chi_phi) & (df["Chi tiết"] == chi_tiet) & (df["Tháng"].dt.year.isin(nam))]["Amt"].sum() / 1e3, 2)
    else:
        ky_nay = round(df[(df["Plant Code"].isin(plant_code)) & (df["Chi Phí"] == chi_phi) & (df["Chi tiết"] == chi_tiet) & (df["Tháng"].dt.month.isin(thang)) & (df["Tháng"].dt.year.isin(nam))]["Amt"].sum() / 1e3, 2)
        lk = round(df[(df["Plant Code"].isin(plant_code)) & (df["Chi Phí"] == chi_phi) & (df["Chi tiết"] == chi_tiet) & (df["Tháng"].dt.month.isin(range(1, max(thang) + 1))) & (df["Tháng"].dt.year.isin(nam))]["Amt"].sum() / 1e3, 2)
        ca_nam = round(df[(df["Plant Code"].isin(plant_code)) & (df["Chi Phí"] == chi_phi) & (df["Chi tiết"] == chi_tiet) & (df["Tháng"].dt.year.isin(nam))]["Amt"].sum() / 1e3, 2)

    return ky_nay, lk, ca_nam

def result_kh(year, month, plant_code='Select All'):
    df = kehoach()
    dthu_tsv, lk_dthu_tsv, kh_cn_dthu_tsv = get_chitieu(df=df, chi_phi="Doanh Thu", chi_tiet="TSV", thang=month, nam=year, plant_code=plant_code) 
    dthu_vm, lk_dthu_vm, kh_cn_dthu_vm  = get_chitieu(df=df, chi_phi="Doanh Thu", chi_tiet="VM", thang=month, nam=year, plant_code=plant_code)
    lgop_tsv, lk_lgop_tsv, kh_cn_lgop_tsv = get_chitieu(df=df, chi_phi="Lãi Gộp", chi_tiet="TSV", thang=month, nam=year, plant_code=plant_code)
    lgop_vm, lk_lgop_vm, kh_cn_lgop_vm = get_chitieu(df=df, chi_phi="Lãi Gộp", chi_tiet="VM", thang=month, nam=year, plant_code=plant_code)
    cpv_tsv, lk_cpv_tsv, kh_cn_cpv_tsv = get_chitieu(df=df, chi_phi="Chi Phí Vốn", chi_tiet="TSV", thang=month, nam=year, plant_code=plant_code)
    cpv_vm, lk_cpv_vm, kh_cn_cpv_vm = get_chitieu(df=df, chi_phi="Chi Phí Vốn", chi_tiet="VM", thang=month, nam=year, plant_code=plant_code)

    # return df[(df["Chi tiết"] == "TSV")]
    cp_luong, lk_cp_luong, kh_cn_cp_luong = get_chitieu(df=df, chi_phi="Chi Phí Lương", chi_tiet="Chi Phí Lương", thang=month, nam=year, plant_code=plant_code)
    cp_mb, lk_cp_mb, kh_cn_cp_mb =  get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP Mặt Bằng", thang=month, nam=year, plant_code=plant_code)
    cp_tscd, lk_cp_tscd, kh_cn_cp_tscd = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP Phân Bổ (KH)", thang=month, nam=year, plant_code=plant_code)
    cp_ccdc, lk_cp_ccdc, kh_cn_cp_ccdc = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP Phân Bổ (CCDC)", thang=month, nam=year, plant_code=plant_code)
    cp_sc, lk_cp_sc, kh_cn_cp_sc = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP Phân Bổ (SC)", thang=month, nam=year, plant_code=plant_code)
    cp_ct, lk_cp_ct, kh_cn_cp_ct = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP chuyển tiền", thang=month, nam=year, plant_code=plant_code)
    cp_cl, lk_cp_cl, kh_cn_cp_cl = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP còn lại", thang=month, nam=year, plant_code=plant_code)
    cp_hc, lk_cp_hc, kh_cn_cp_hc = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP hành chính", thang=month, nam=year, plant_code=plant_code)
    cp_km, lk_cp_km, kh_cn_cp_km = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP khuyến mãi", thang=month, nam=year, plant_code=plant_code)
    cp_mkt, lk_cp_mkt, kh_cn_cp_mkt = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP marketing", thang=month, nam=year, plant_code=plant_code)
    cp_vlp, lk_cp_vlp, kh_cn_cp_vlp = get_chitieu(df=df, chi_phi="Chi Phí Ngoài Lương", chi_tiet="CP vật liệu phụ", thang=month, nam=year, plant_code=plant_code)
    tong_cpnl = cp_mb + cp_tscd + cp_ccdc + cp_sc + cp_ct + cp_cl + cp_hc + cp_km + cp_mkt + cp_vlp
    lk_tong_cpnl = lk_cp_mb + lk_cp_tscd + lk_cp_ccdc + lk_cp_sc + lk_cp_ct + lk_cp_cl + lk_cp_hc + lk_cp_km + lk_cp_mkt + lk_cp_vlp
    kh_cn_tong_cpnl = kh_cn_cp_mb + kh_cn_cp_tscd + kh_cn_cp_ccdc + kh_cn_cp_sc + kh_cn_cp_ct + kh_cn_cp_cl + kh_cn_cp_hc + kh_cn_cp_km + kh_cn_cp_mkt + kh_cn_cp_vlp

    tong_cp = cp_luong + tong_cpnl
    lk_tong_cp = lk_cp_luong + lk_tong_cpnl
    kh_cn_tong_cp = kh_cn_cp_luong + kh_cn_tong_cpnl

    lntt = lgop_tsv + lgop_vm - cpv_tsv - cpv_vm - tong_cp
    lk_lntt = lk_lgop_tsv + lk_lgop_vm - lk_cpv_tsv - lk_cpv_vm - lk_tong_cp
    kh_cn_lntt = kh_cn_lgop_tsv + kh_cn_lgop_vm - kh_cn_cpv_tsv - kh_cn_cpv_vm - kh_cn_tong_cp
    
    kehoach_kynay = pd.DataFrame(
        {
            'Chỉ Tiêu': ['Doanh thu', '- TSV ', '- VM ', 'Lãi Gộp', '- TSV  ', '- VM  ', "Chi Phí Vận Hành", "+ Chi Phí Nhân Viên", \
                "+ Chi Phí Ngoài Lương", '- CP CCDC', '- CP KH TSCĐ', '- CP vật liệu phụ', '- CP Còn lại', '- CP Thuê ngoài', \
                    '- CP hành chính', '- CP chuyển tiền', '- CP Marketing & Khuyến mãi', '- CP sửa chữa, bảo trì', 'Chi Phí Vốn', \
                        '- TSV   ', '- VM   ', 'LNTT', 'LNTT(-VM)', 'LNST', 'LNST(-VM)'],
            'Kế Hoạch': [dthu_tsv + dthu_vm, dthu_tsv, dthu_vm, lgop_tsv + lgop_vm, lgop_tsv, lgop_vm, \
                tong_cp, cp_luong, tong_cpnl, cp_ccdc, cp_tscd, cp_vlp, cp_cl, cp_mb, cp_hc, cp_ct, \
                    cp_mkt + cp_km, cp_sc, cpv_tsv + cpv_vm,cpv_tsv, cpv_vm, lntt, lntt - lgop_vm + cpv_vm, lntt * 0.8, (lntt - lgop_vm + cpv_vm) * 0.8],
            'LK Kế Hoạch': [lk_dthu_tsv + lk_dthu_vm, lk_dthu_tsv, lk_dthu_vm, lk_lgop_tsv + lk_lgop_vm, lk_lgop_tsv, lk_lgop_vm, \
                lk_tong_cp, lk_cp_luong, lk_tong_cpnl, lk_cp_ccdc, lk_cp_tscd, lk_cp_vlp, lk_cp_cl, lk_cp_mb, lk_cp_hc, lk_cp_ct, \
                    lk_cp_mkt + lk_cp_km, lk_cp_sc, lk_cpv_tsv + lk_cpv_vm, lk_cpv_tsv, lk_cpv_vm, lk_lntt, lk_lntt - lk_lgop_vm + lk_cpv_vm, lk_lntt * 0.8, (lk_lntt - lk_lgop_vm + lk_cpv_vm) * 0.8],
            'KH Năm': [kh_cn_dthu_tsv + kh_cn_dthu_vm, kh_cn_dthu_tsv, kh_cn_dthu_vm, kh_cn_lgop_tsv + kh_cn_lgop_vm, kh_cn_lgop_tsv, kh_cn_lgop_vm, \
                kh_cn_tong_cp, kh_cn_cp_luong, kh_cn_tong_cpnl, kh_cn_cp_ccdc, kh_cn_cp_tscd, kh_cn_cp_vlp, kh_cn_cp_cl, kh_cn_cp_mb, kh_cn_cp_hc, kh_cn_cp_ct, \
                    kh_cn_cp_mkt + kh_cn_cp_km, kh_cn_cp_sc, kh_cn_cpv_tsv + kh_cn_cpv_vm, kh_cn_cpv_tsv, kh_cn_cpv_vm, kh_cn_lntt, kh_cn_lntt - kh_cn_lgop_vm + kh_cn_cpv_vm, kh_cn_lntt * 0.8, (kh_cn_lntt - kh_cn_lgop_vm + kh_cn_cpv_vm) * 0.8]
        }
    )
    return kehoach_kynay