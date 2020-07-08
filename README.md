## Project: Database Exploration
#### This is my final project at Spiced Academy. I wanted to compare different databases and use some tools, which are not part of the Spiced curriculum. The idea came from the book "Seven Databases in Seven Weeks" by Luc Perkins. Since I'm having only two weeks, I'm doing 6 databases and use them in a simplified manner.
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


### Learnings MySQL
* Setting up MySQL 1st time really hard:
  * easy access via Docker CLI
  * Connecting db to MySQL Workbench -> create an (just another) Oracle account
  * allow specific IP's instead of localhost
  * giving users privileges

* reading from pandas to_sql takes a lot of time to upload data to MySQL
##### Why you maybe like MySQL
* MySQL Workbench super cool tool
  * easy to maintain, import/export data, visualization of data
  * schema is synonymous with a database

----

### Learnings Postgres
* easier to use than MySQL
* free GUI Tools like Postico (not that much functionality like Workbench)

---
### Learnings MongoDB
* easy set up
* free Monitoring with unique URL

---
### Learnings HBase
* no official Docker Image
* for really(!) Big Data
* need to know Ruby or Java
* data insertion not the best
* indexes with timestamps by itself
* rows are similar to Python dictionaries

---
### Performance
* MySQl performance:
* 2047078 row(s) returned	0.024 sec (Duration)/ 38.171 sec (Fetch time)
