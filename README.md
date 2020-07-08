## Project: Database Exploration / Pipeline
#### This is my final project at Spiced Academy. I wanted to compare different databases and use some tools, which are not part of the Spiced curriculum. The idea came from the book "Seven Databases in Seven Weeks" by Luc Perkins. Since I'm having only two weeks, I'm doing 4 databases and use them in a pipeline so it's more of "RL problem". I wanted to use Apache Spark to show how pandas breaks with big data.
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

![image](https://github.com/fe-bern/db_exploration/blob/master/img/architecture.png?raw=true)


### Learnings from working with different databases
----

| Databases  |  MySQL |  Postgres | MongoDB  | Redis  |
|---|---|---|---|---|
| Pros  | MySQL Workbench super cool tool, easy to maintain, import/export data, visualization of data, schema is synonymous with a database  | easier to use than MySQL, free GUI Tools like Postico (not that much functionality like Workbench)  | easy set up, free Monitoring with unique URL |   |
| Cons  | Connecting db to MySQL Workbench, create an (just another) Oracle account, allow specific IP's instead of localhost, giving users privileges  |   |   |   |


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
  * `SELECT * FROM table1`: 2.047.078 row(s) returned	0.024 sec (Duration)/ 38.171 sec (Fetch time)
