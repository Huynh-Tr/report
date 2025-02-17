import pandas as pd
from glob import glob
import os
import requests

def kh2025():
    
    path = r"D:\pnj.com.vn\HuynhTN - Documents\2025\Planning"
    file2025 = os.path.join(path, "Planning2025.xlsx")
    file2025 = pd.read_excel(file2025, sheet_name="Budget_Total", header=1)
    file2025 = file2025[file2025["Tháng"].isin(range(1, 13))]
    col = ["T", "9999"]
    file2025 = file2025.drop(columns=col)
    # unstack the dataframe keep 3 first columns
    file2025 = file2025.set_index(['Chi Phí', 'Chi tiết', 'Tháng']).stack().reset_index(name='Amt')
    
    return kh2025