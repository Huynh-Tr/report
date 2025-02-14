import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from glob import glob
import os


def create_parquet_file(csv_files, parquet_file):
    pd_df = pd.concat([pd.read_csv(csv_file) for csv_file in csv_files])
    table = pa.Table.from_pandas(pd_df)
    pq.write_table(table, parquet_file)

# dthu parquet
parquet_file = ['dthu.parquet', 'cphi.parquet', 'others.parquet', 'tonkho.parquet']
path = "D:\pnj.com.vn\HuynhTN - Documents\Data\DataBI"
csv_list_files = ([glob(os.path.join(path, "Dthu\\*.csv")),
                  glob(os.path.join(path, "CP\\*.csv")),
                  glob(os.path.join(path, "Others\\*.csv")),
                  glob(os.path.join(path, "TK\\*.csv"))])
output_path = "D:\pnj.com.vn\HuynhTN - Documents\Project\streamlit"
parquet_file = [os.path.join(output_path, file) for file in parquet_file]

print(parquet_file)

for output_file, csv_files in zip(parquet_file, csv_list_files):
    print(output_file)
    if not os.path.exists(output_file):
        pd_df = pd.concat([pd.read_csv(csv_file) for csv_file in csv_files])
        table = pa.Table.from_pandas(pd_df)
        pq.write_table(table, output_file)