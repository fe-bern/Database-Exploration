'''Loading Data from MySQL and transforming it. Later it's saved in Postgres and MongoDB.'''

import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import logging
import psycopg2
import time
import pymongo
# from redis import StrictRedis
# from redis_cache import RedisCache
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, LongType, TimestampType, ShortType, DateType
from pyspark.sql.functions import col

time.sleep(15) #waiting for mysql to be ready

#MySQL engine
load_dotenv()
mysql_user = os.getenv('MYSQL_USER')
mysql_password= os.getenv('MYSQL_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = os.getenv('MYSQL_PORT')
conns_mysql = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/bitmex_data"
engine_mysql = create_engine(conns_mysql, encoding="latin1", echo=True)

#Postgres engine
load_dotenv()
psql_user = os.getenv('PSQL_USER')
psql_password= os.getenv('PSQL_PASSWORD')
psql_host = os.getenv('PSQL_HOST')
psql_port = os.getenv('PSQL_PORT')
conns_psql = f"postgresql://{psql_user}:{psql_password}@{psql_host}:{psql_port}/bitmex_data2"
engine_psql = create_engine(conns_psql, encoding="latin1", echo=True)

#MongoDB connection
conn = "mongodb"
client = pymongo.MongoClient(conn)
db = client.bitmex
collection_ethereum = db.bitmex_ethereum
collection_bitcoin = db.bitmex_bitcoin

#Redis Conneection
# client_redis = StrictRedis(host="redis", decode_responses=True)
# cache = RedisCache(redis_client=client_redis)


def loading_and_storing_eth():
    '''Loads from MySQL and stores ETHUSD in Postgres'''
    query = "SELECT * FROM table_bitmex WHERE symbol='ETHUSD';"
    ethereum = engine_mysql.execute(query)
    ethereum = pd.DataFrame(ethereum)
    ethereum.to_sql('table_ethereum', con=engine_psql, if_exists='replace', method='multi')
    return ethereum

#gives OOM Error
# def loading_and_storing_xbt():
#     '''Loads from MySQL and stores XBTUSD in Postgres'''
#     query = "SELECT * FROM table_bitmex WHERE symbol='XBTUSD';"
#     bitcoin = engine_mysql.execute(query)
#     bitcoin = pd.DataFrame(bitcoin)
#     bitcoin.to_sql('table_bitcoin', con=engine_psql, if_exists='replace', method='multi')
#     return bitcoin

def spark_job():
    #Placeholder -maybe something with PySpark
    def initialize_Spark():
        spark = SparkSession.builder \
            .master("local[*]") \
            .appName("simple spark usage") \
            .getOrCreate()
        return spark

    spark = initialize_Spark()

    def loadDFWithoutSchema(spark):
        df = spark.read.format("csv").option("header", "true").load("out_file.csv")
        return df

    def clean_drop_data(df):
        df_dropped = df.drop("bidSize","askSize")
        df_final = df_dropped[df_dropped["symbol"] == "XBTZ20"]
        return df_final

    def load_to_postgres(df_final):
        df_final.to_sql('table_xbt_dec', con=engine_psql, if_exists='replace', method='multi')

# @cache.cache()
def transform_eth():
    '''extract Ethereum from Postgres and store it in MongoDB'''
    query = "SELECT * FROM table_ethereum;"
    ethereum = engine_psql.execute(query)
    ethereum = pd.DataFrame(ethereum)
    daily_max_eth = int(ethereum[5].max())
    daily_min_eth = int(ethereum[5].min())
    eth_stats = {"Max askPrice": daily_max_eth,
                 "Min askPrice": daily_min_eth}
    collection_ethereum.insert(eth_stats)
    logging.critical('Insert Ethereum in MongoDB complete')
    print(collection_ethereum)

# def transform_xbt():
#     '''extract Bitcoin from Postgres and store it in MongoDB'''
#     query = "SELECT * FROM table_bitcoin;"
#     bitcoin = engine_psql.execute(query)
#     bitcoin = pd.DataFrame(bitcoin)
#     daily_max_xbt = bitcoin.askPrice.max()
#     daily_min_xbt = bitcoin.askPrice.min()
#     collection_bitcoin.insert(daily_max_xbt, daily_min_xbt)
#     logging.critical('Insert Bitcoin in MongoDB complete')

#no function gets executed, because airflow replaces the script
logging.critical('starting process')
logging.critical('Start storing to postgres')
#loading_and_storing_eth()
#loading_and_storing_xbt()
logging.critical('Finished storing')
logging.critical('starting transforming')
#transform_eth()
#transform_xbt()
#spark_job()
logging.critical('Program Exit')
