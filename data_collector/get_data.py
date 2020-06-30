'''Collecting Data and storing in as DF in MySQL'''

import gzip
import pandas as pd
import requests
from datetime import date
import urllib.request

aws_url = "https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/quote/"
file_ending = ".csv.gz"

def get_recent_url():
    today = date.today().strftime("%Y%M%D").replace("/", "")
    new_today = today[:3] + today[5:10]
    new_today = str(int(new_string) - 2)
    url_data = aws_url + new_today + file_ending
    return url_data

def download_file(url):
   out_file = '/Users/felixberner/Desktop/finalproject/data/out_file.csv'

   # Download archive
   try:
      # Read the file inside the .gz archive located at url
      with urllib.request.urlopen(url) as response:
         with gzip.GzipFile(fileobj=response) as uncompressed:
            file_content = uncompressed.read()

      # write to file in binary mode 'wb'
      with open(out_file, 'wb') as f:
         f.write(file_content)
         return 0

   except Exception as e:
      print(e)
      return 1

get_recent_url()
download_file(url_data)
