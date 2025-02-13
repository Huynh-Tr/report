import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from glob import glob  # For handling multiple CSV files
import os

path = "D:\pnj.com.vn\HuynhTN - Documents\Project\streamlit"

csv_files = glob(os.path.join(path, "Dthu\\*.csv"))  # Get all CSV files in the directory
# create a directory to save parquet files
if not os.path.exists(os.path.join(path, "dthu_parquet_files")):
    os.makedirs(os.path.join(path, "dthu_parquet_files"))

parquet_directory = os.path.join(path, "dthu_parquet_files")

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    table = pa.Table.from_pandas(df)

    # Create parquet filename based on csv filename:
    parquet_file = parquet_directory + "\\" + os.path.basename(csv_file).replace('.csv', '.parquet')

    pq.write_table(table, parquet_file)