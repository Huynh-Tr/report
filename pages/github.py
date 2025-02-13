import pandas as pd
import requests
from io import StringIO
import streamlit as st
from glob import glob

# glob github files
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

files = load_github_files()
df = pd.concat([pd.read_csv(file) for file in files])
st.write(df)

# # st.write(files)
# def load_original_data():
#     url = 'https://raw.githubusercontent.com/Huynh-Tr/report/refs/heads/main/Dthu/202101.csv'
#     response = requests.get(url)
#     if response.status_code == 200:
#         return pd.read_csv(StringIO(response.text))
#     else:
#         st.error("Failed to load data from GitHub.")
#         return None

# df = load_original_data()
# st.write(df)