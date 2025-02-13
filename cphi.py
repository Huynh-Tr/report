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

cphi_parquet = r"https://raw.githubusercontent.com/Huynh-Tr/report/main/cphi.parquet"

def cphi():        
    df = pd.read_parquet(cphi_parquet)
    df_cp = df[df["Month year"] != "Month year"]
    df_cp["Month year"] = pd.to_datetime(df_cp["Month year"]).dt.to_period('M')

    # create MaCH column with condition right 4 chartacters of cost center code if not null else right 4 characters of GL Account Code
    df_cp["MaCH"] = df_cp["Cost Center Code"].fillna(df_cp["Plant Code"].astype('str')).astype('int').astype('str').str[-4:] \
        .replace('0000', 'P015').replace('9999', 'P015')

    df_cp["FM. Loc Amt"] = df_cp["FM. Loc Amt"].astype('float')

    cols = ["Month year", "GL Account Code", "GL LV1 Name", "FM. Loc Amt", "PnL Name", "MaCH"]
    gl_code_exl = 64110120 # list of GL Account Code
    gl_code_range = [64100000, 64252100]

    # filter data cols with gl_code_exl and in range gl_code_range
    df_cp = df_cp[cols][(df_cp["GL Account Code"] != gl_code_exl) & (df_cp["GL Account Code"].between(gl_code_range[0], gl_code_range[1]))]

    return df_cp