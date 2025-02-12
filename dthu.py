import pandas as pd 
from glob import glob
import os
import requests

import warnings
warnings.filterwarnings("ignore")

def load_github_files():
    url = 'https://api.github.com/repos/Huynh-Tr/report/contents/Dthu'
    response = requests.get(url)
    if response.status_code == 200:
        files = pd.DataFrame(response.json())
        files['name'] = files['name'].str.replace('.csv', '')
        return files['download_url'].tolist()
    else:
        st.error("Failed to load data from GitHub.")
        return None
        
def dthu():
    # path = "D:\pnj.com.vn\HuynhTN - Documents\Data\DataBI"
    # files_Dthu = glob(os.path.join(path, "Dthu\\*.csv"))
    files_Dthu = load_github_files()

    df = pd.concat([pd.read_csv(file, encoding='utf-8', sep=',', header=0) for file in files_Dthu])
    df["Month year"] = pd.to_datetime(df["Month year"]).dt.strftime('%m-%Y')
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
