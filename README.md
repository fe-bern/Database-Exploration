## Project: Database Exploration / Pipeline

![Python application](https://github.com/fe-bern/db_exploration/workflows/Python%20application/badge.svg)

#### This is my final project at Spiced Academy. I wanted to compare different databases and use some tools, which are not part of the Spiced curriculum. The idea came from the book "Seven Databases in Seven Weeks" by Luc Perkins. The other part of my project is building a pipeline and connecting it to different database. I wanted to use Apache Spark to show how pandas breaks with big data.
---
### Goal:
* Setting up a Data Collector
* Connecting to different databases:
  * `MySQL`
  * `Postgres`
  * `MongoDB`
  * `Redis`
  * (`HBase`)
* Using `Apache Spark` for analyzing the data
* Connecting everything via `Docker`
* Orchestrated with `Airflow`

![image](https://github.com/fe-bern/db_exploration/blob/master/img/architecture_new.png?raw=true)


### Learnings from working with different databases
----

|  MySQL |  Postgres | MongoDB  | Redis  |
|---|---|---|---|
| MySQL Workbench very useful, easy to maintain, import/export data, visualization of data | easier to use than MySQL, free GUI Tools like Postico (not that much functionality like Workbench), but quick check for content  | easy set up, free Monitoring with unique URL | not really a Database, Key-Value-Storage, Caches other DB's  |


---
### Learnings from HBase
* no official Docker Image
* for really(!) Big Data
* need to know Ruby or Java
* data insertion not the best
* indexes with timestamps by itself
* rows are similar to Python dictionaries

---
### Performance
* MySQl performance:
  * `%time pd.to_sql`: CPU times: user 1min 33s, sys: 24.2 s, total: 1min 57s Wall time: 5min 14s
  * `SELECT * FROM table1`: 2.047.078 row(s) returned	0.024 sec (Duration)/ 38.171 sec (Fetch time)
* Postgres Performance:
  * `%time pd.to_sql`: interrupted the kernel after over an hour, table is created but no data is inserted (even with `echo=True` and `INSERT` is executed)

---
* Apache Spark maybe a bit overkill, clusters also quite complex instead using PySpark
