'''Collecting Data and storing in as DF in MySQL'''

from csv import reader
from io import StringIO
import gzip
import pandas as pd

with gzip.open("20160826.csv.gz", "rb") as f:
    file_content = f.read()
data = file_content.decode("utf-8")
data = StringIO(data)
df = pd.read_csv(data)
print(df.head(5))
