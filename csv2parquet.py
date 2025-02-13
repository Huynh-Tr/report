import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from glob import glob
import os

# Create an Arrow table with an empty schema
parquet_file = 'output.parquet'
table = pa.Table.from_pandas(pd.DataFrame())
# pq.write_table(table, parquet_file)

# Path = "D:\pnj.com.vn\HuynhTN - Documents\Project\streamlit"
path = "D:\pnj.com.vn\HuynhTN - Documents\Project\streamlit"
csv_files = glob(os.path.join(path, "Dthu\\*.csv"))  # Get all CSV files in the directory

pd_df = pd.concat([pd.read_csv(csv_file) for csv_file in csv_files])
table = pa.Table.from_pandas(pd_df)
pq.write_table(table, parquet_file)