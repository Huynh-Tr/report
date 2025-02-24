import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from glob import glob
import os

output_path = "D:\pnj.com.vn\HuynhTN - Documents\Project\streamlit"

path = "D:\pnj.com.vn\HuynhTN - Documents\Data\DataBI"
parquet_file = ['dthu.parquet', 'cphi.parquet', 'others.parquet', 'tonkho.parquet']
csv_list_files = ([glob(os.path.join(path, "Dthu\\*.csv")),
                  glob(os.path.join(path, "CP\\*.csv")),
                  glob(os.path.join(path, "Others\\*.csv")),
                  glob(os.path.join(path, "TK\\*.csv"))])
parquet_file = [os.path.join(output_path, file) for file in parquet_file]

path_kh = "D:\pnj.com.vn\HuynhTN - Documents\Data\Planning"
excel_list_files_kh = glob(os.path.join(path_kh, "*.xlsx"))
parquet_file_kh = os.path.join(output_path, 'kh.parquet')

path_03h = "D:\pnj.com.vn\HuynhTN - Documents\Data\SAP (FAGLL03H)"
excel_list_files_03h = glob(os.path.join(path_03h, "*.xlsx"))
parquet_file_03h = os.path.join(output_path, '03h.parquet')


def datamodelss():
    for output_file, csv_files in zip(parquet_file, csv_list_files):
        if not os.path.exists(output_file):
            pd_df = pd.concat([pd.read_csv(csv_file) for csv_file in csv_files])
            table = pa.Table.from_pandas(pd_df)
            pq.write_table(table, output_file)
        else:
            os.remove(output_file)
            pd_df = pd.concat([pd.read_csv(csv_file) for csv_file in csv_files])
            table = pa.Table.from_pandas(pd_df)
            pq.write_table(table, output_file)

def kh():
    df = pd.DataFrame()
    for file in excel_list_files_kh:
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
    if not os.path.exists(parquet_file_kh):
        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_file_kh)
    else:
        os.remove(parquet_file_kh)
        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_file_kh)

# def fagll03h():
#     df = pd.DataFrame()
#     df = pd.concat([pd.read_excel(f) for f in files], ignore_index=True)
#     df['Posting Date'] = pd.to_datetime(df['Posting Date']).dt.date
#     df['Payment reference'] = df['Payment reference'].astype(str).str.replace('.0', '')
#     df['Document Number'] = df['Document Number'].astype(str).str.replace('.0', '')
#     df['Cost Center'] = df['Cost Center'].astype(str).str.replace('.0', '')
#     df['Asset'] = df['Asset'].astype(str).str.replace('.0', '')
#     cols = ["Company Code Currency Key", "Material", "Sales Document", "Billing Document", "Quantity", "Unit of Measure", "Order"]
#     df = df.drop(columns=cols)

def fagll03h():
    df = pd.concat([pd.read_excel(f) for f in excel_list_files_03h], ignore_index=True)
    df['Posting Date'] = pd.to_datetime(df['Posting Date']).dt.date
    df['Payment reference'] = df['Payment reference'].astype(str).str.replace('.0', '')
    df['Document Number'] = df['Document Number'].astype(str).str.replace('.0', '')
    df['Cost Center'] = df['Cost Center'].astype(str).str.replace('.0', '')
    df['Asset'] = df['Asset'].astype(str).str.replace('.0', '')
    cols = ["Company Code Currency Key", "Material", "Sales Document", "Billing Document", "Quantity", "Unit of Measure", "Order"]
    df = df.drop(columns=cols)

    if not os.path.exists(parquet_file_03h):
        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_file_03h)
    else:
        os.remove(parquet_file_03h)
        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_file_03h)

def main():
    # datamodelss()
    # kh()
    fagll03h()

if __name__ == "__main__":
    main()