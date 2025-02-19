import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from glob import glob
import os


# def create_parquet_file_csv(csv_files, parquet_file):
#     pd_df = pd.concat([pd.read_csv(csv_file) for csv_file in csv_files])
#     table = pa.Table.from_pandas(pd_df)
#     pq.write_table(table, parquet_file)

# def create_parquet_file_excel(excel_files, parquet_file):
#     pd_df = pd.concat([pd.read_excel(excel_file, sheet_name="Budget_Total", header=1) for excel_file in excel_files])
#     table = pa.Table.from_pandas(pd_df)
#     pq.write_table(table, parquet_file)

# parquet
parquet_file = ['dthu.parquet', 'cphi.parquet', 'others.parquet', 'tonkho.parquet', 'kh.parquet']
path = "D:\pnj.com.vn\HuynhTN - Documents\Data\DataBI"
path_kh = "D:\pnj.com.vn\HuynhTN - Documents\Data\Planning"

csv_list_files = ([glob(os.path.join(path, "Dthu\\*.csv")),
                  glob(os.path.join(path, "CP\\*.csv")),
                  glob(os.path.join(path, "Others\\*.csv")),
                  glob(os.path.join(path, "TK\\*.csv"))])

excel_list_files = [glob(os.path.join(path_kh, "*.xlsx"))]

output_path = "D:\pnj.com.vn\HuynhTN - Documents\Project\streamlit"
parquet_file = [os.path.join(output_path, file) for file in parquet_file[:-1]]
parquet_file_kh = os.path.join(output_path, parquet_file[-1])

print(parquet_file_kh)

for output_file, csv_files in zip(parquet_file, csv_list_files):
    print(output_file)
    if not os.path.exists(output_file):
        pd_df = pd.concat([pd.read_csv(csv_file) for csv_file in csv_files])
        table = pa.Table.from_pandas(pd_df)
        pq.write_table(table, output_file)

if not os.path.exists(parquet_file_kh):
    df = pd.DataFrame()
    for file in excel_list_files:
        # print(file)
        pd_df = pd.read_excel(file, sheet_name="Budget_Total", header=1)
        pd_df = pd_df[pd_df["Tháng"].isin(range(1, 13))]
        col = ["T", "9999", "VP"]
        pd_df = pd_df.drop(columns=col)
        # unstack the dataframe keep 3 first columns name level_3 is Plant Code
        pd_df = pd_df.set_index(['Chi Phí', 'Chi tiết', 'Tháng']).stack().reset_index(name='Amt')
        pd_df = pd_df.rename(columns={"level_3": "Plant Code"})
        pd_df.groupby(["Chi Phí", "Chi tiết"])["Amt"].sum().reset_index()
        pd_df = pd_df[pd_df['Amt'] != 0]
        pd_df["Tháng"] = pd.to_datetime(pd_df["Tháng"].astype('str') + '-' + file[-9:-5]).dt.to_period('M')
        pd_df["Plant Code"] = pd_df["Plant Code"].astype(str)
        df = pd.concat([df, pd_df])
    # print(df["Tháng"].unique())
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_file_kh)
