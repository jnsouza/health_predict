import os
import wget
import zipfile
import subprocess
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

## file names
file_zip = 'LLCP2023XPT.zip'
file_XPT = 'LLCP2023.XPT '
file_csv = 'LLCP2023.csv'


## file paths
current_path = os.path.join(os.getcwd(), "raw")
zip_path     = os.path.join(current_path, file_zip)
XPT_path     = os.path.join(current_path, file_XPT)


## loading file
print("1/3 Downloading file")
url = f'https://www.cdc.gov/brfss/annual_data/2023/files/{file_zip}'
wget.download(url, zip_path)


## unzip file
print("2/3 Unziping files")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(current_path)


## converting to .csv
print("3/3 Converting to .csv")
file_path = os.path.join(current_path, file_XPT)
df        = pd.read_sas(file_path, format='xport', encoding='latin1')
csv_path  = os.path.join(current_path, file_csv)
df.to_csv(csv_path, index=False)

print(f"Data converted to .csv in {csv_path}!")


## removing XPT, .zip
os.remove(XPT_path)
os.remove(zip_path)
