"""Script for Airflow pipeline, this is used instead of transform_data.py"""

import os
import time
from datetime import datetime, timedelta
import logging
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import pymongo

from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


# Setting default args
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 7, 14),  # year, month, day
    "email": ["your_mail_adress@mail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    # 'end_date': datetime(2016, 1, 1),
}

# creating dag
dag = DAG("etl", default_args=default_args, schedule_interval=timedelta(minutes=1))

# MySQL engine
load_dotenv()
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
conns_mysql = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/bitmex_data"
engine_mysql = create_engine(conns_mysql, encoding="latin1", echo=True)

# Postgres engine
load_dotenv()
psql_user = os.getenv("PSQL_USER")
psql_password = os.getenv("PSQL_PASSWORD")
psql_host = os.getenv("PSQL_HOST")
psql_port = os.getenv("PSQL_PORT")
conns_psql = f"postgresql://{psql_user}:{psql_password}@{psql_host}:{psql_port}/bitmex_data2"
engine_psql = create_engine(conns_psql, encoding="latin1", echo=True)

# MongoDB connection
conn = "mongodb"
client = pymongo.MongoClient(conn)
db = client.bitmex
collection_ethereum = db.bitmex_ethereum
collection_bitcoin = db.bitmex_bitcoin

# extract from MySQL
def extract_from_mysql():
    query = "SELECT * FROM table_bitmex;"
    ethereum = engine_mysql.execute(query)
    ethereum_df = pd.DataFrame(ethereum)
    print(ethereum_df.axes)
    return ethereum_df


# transform
def transform_big_to_smaller(**context):
    extract_connection = context["task_instance"]
    ethereum_df = extract_connection.xcom_pull(task_ids="extract_from_mysql")
    ethereum_final = ethereum_df.drop([3, 5], axis=1)
    ethereum_final = ethereum_final[ethereum_final[2] == "ETHUSD"]
    logging.critical("transform complete")
    return ethereum_final


# load to Postgres
def load_smaller_to_postgres(**context):
    extract_connection = context["task_instance"]
    ethereum_final = extract_connection.xcom_pull(task_ids="transform_big_to_smaller")
    ethereum_final.to_sql(
        "table_ethereum", con=engine_psql, if_exists="replace", method="multi"
    )


# transform 2
def transform_only_stats(**context):
    extract_connection = context["task_instance"]
    ethereum_final = extract_connection.xcom_pull(task_ids="transform_big_to_smaller")
    ethereum_final = pd.DataFrame(ethereum_final)
    daily_max_eth = int(ethereum_final[6].max())
    daily_min_eth = int(ethereum_final[6].min())
    eth_stats = {"Max askPrice": daily_max_eth, "Min askPrice": daily_min_eth}
    return eth_stats


# load to MongoDB
def load_stats_to_mongodb(**context):
    extract_connection = context["task_instance"]
    eth_stats = extract_connection.xcom_pull(task_ids="transform_only_stats")
    collection_ethereum.insert(eth_stats)
    logging.critical("Insert Ethereum in MongoDB complete")


# create extract task
extract_from_mysql = PythonOperator(
    task_id="extract_from_mysql",
    python_callable=extract_from_mysql,
    dag=dag
)

# create transform task
transform_big_to_smaller = PythonOperator(
    task_id="transform_big_to_smaller",
    python_callable=transform_big_to_smaller,
    provide_context=True,
    dag=dag,
)

# create load task
load_smaller_to_postgres = PythonOperator(
    task_id="load_smaller_to_postgres",
    python_callable=load_smaller_to_postgres,
    provide_context=True,
    dag=dag,
)

# create transform2 task
transform_only_stats = PythonOperator(
    task_id="transform_only_stats",
    python_callable=transform_only_stats,
    provide_context=True,
    dag=dag,
)

# create load2 task
load_stats_to_mongodb = PythonOperator(
    task_id="load_stats_to_mongodb",
    python_callable=load_stats_to_mongodb,
    provide_context=True,
    dag=dag,
)

# dependencies
extract_from_mysql >> transform_big_to_smaller >> load_smaller_to_postgres >> transform_only_stats >> load_stats_to_mongodb
