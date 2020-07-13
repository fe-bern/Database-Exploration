'''Collecting Data and storing as DF in MySQL'''

from datetime import date
import urllib.request
import gzip
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import logging
import time
import mysql.connector


AWS_URL = "https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/quote/"
FILE_ENDING = ".csv.gz"
OUT_FILE = 'out_file.csv'

def get_recent_url():
    '''Get newest data, data has a delay of 2 days.'''
    today = date.today().strftime("%Y%M%D").replace("/", "")
    new_today = today[:3] + today[5:10]
    new_today = str(int(new_today) - 2)
    url_data = AWS_URL + new_today + FILE_ENDING
    return url_data

def download_file(url):
    '''Downloads the gz file and write the content to a csv file.'''
    # Download archive
    try:
        # Read the file inside the .gz archive located at url
        with urllib.request.urlopen(url) as response:
            with gzip.GzipFile(fileobj=response) as uncompressed:
                file_content = uncompressed.read()

        # write to file in binary mode 'wb'
        with open(OUT_FILE, 'wb') as f:
            f.write(file_content)
            return 0

    except Exception as e:
        print(e)
        return 1

def storing_in_mysql(out_file):
    '''Transforms the csv file to a DF and reads at in MySQL'''
    #setting up connection to MySQL
    load_dotenv()
    mysql_user = os.getenv('MYSQL_USER')
    mysql_password= os.getenv('MYSQL_PASSWORD')
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_port = os.getenv('MYSQL_PORT')
    conns = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/bitmex_data"
    engine = create_engine(conns, encoding="latin1", echo=True)

    #reading in file and store it in MySQL
    data = pd.read_csv(out_file)
    data.to_sql('table_bitmex', con=engine, if_exists='replace')


logging.critical('starting process')
download_file(get_recent_url())
logging.critical('downloading subprocess finished')
#storing_in_mysql(OUT_FILE) commented out because MySQL local gets an OOM Error otherwise
logging.critical('storing subprocess finished')
logging.critical('ending process')
