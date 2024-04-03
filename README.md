# stedi_human_balance_analytics
Udacity Nanodegree Data Engineering with AWS Project 3




## 0. Overview

This represents project 3 of the Udacity Nanodegree _Data Engineering with AWS Project 3_. The background of the project as per the assignment description is outlined below:

_The STEDI Team has been hard at work developing a hardware STEDI Step Trainer that:

- trains the user to do a STEDI balance exercise;
- and has sensors on the device that collect data to train a machine-learning algorithm to detect steps;
- has a companion mobile app that collects customer data and interacts with the device sensors.
STEDI has heard from millions of early adopters who are willing to purchase the STEDI Step Trainers and use them.

Several customers have already received their Step Trainers, installed the mobile application, and begun using them together to test their balance. The Step Trainer is just a motion sensor that records the distance of the object detected. The app uses a mobile phone accelerometer to detect motion in the X, Y, and Z directions.

The STEDI team wants to use the motion sensor data to train a machine learning model to detect steps accurately in real-time. Privacy will be a primary consideration in deciding what data can be used.

Some of the early adopters have agreed to share their data for research purposes. Only these customers’ Step Trainer and accelerometer data should be used in the training data for the machine learning model._



## 0.1. Worfklow

The worklow of the project contains the following steps:
- 1. Create AWS Ressources
- 2. Landing Zone
- 3. Trusted Zone
- 4. Curated Zone
- 5. Delete AWS Ressources

An high-level overview of these steps was created with _drawio_ and is stored as: 
- project_overview.png

## 0.2. Source Data

The source data are located here:

s3://cd0030bucket/customers/
s3://cd0030bucket/step_trainer/
s3://cd0030bucket/accelerometer/

## 0.3. S3 Buckets

I set up the following _AWS S3 bucket_ as a target for the data output:
s3://p3-stedi-lakehouse/

Subdirectories indicate the data source and lakehouse zone, e.g.,
s3://p3-stedi-lakehouse/customer/landing/
All output and intermediate data were stored in the respective subdirectory. The data which comprise the final table (_machine_learning_curated_) are stored in:
s3://p3-stedi-lakehouse/machine_learning/curated/

## 3. Landing Zone
I used the _AWS Glue data catalog_ to define the landing tables. The table schema can be found in /DDL:
- customer_landing.sql
- accelerometer_landing.sql
- step_trainer_landing.sql

In addition, their columns and datatypes are stored as .json files with the respective table name in:
- 01_landing/

The created tables are queried with _AWS Athena_. The result is stored in /Screenshots. For each of the sources: 
- customer
- accelerometer
- step_trainer
I stored the output of a sample query:
- table_name.png
and queries which count the number of observations in the tables:
- table_name_count.png

## 4. Trusted Zone

The AWS Glue scripts which depict the jobs which created the output are stored here /02_trusted. The output tables and their schema were via the Glue job (option _Create a table in the Data Catalog and, on subsequent runs, update the schema and add new partitions_) using no compression.


### Customer_Trusted
This table contains only the customers who agreed to share their data for research purposes. The script of the glue job is stored in:
- 02_trusted/customer_landing_to_trusted.py

Query results are stored as:
- _screenshots/customer_landing_trusted.png
- _screenshots/customer_landing_trusted_count.png
    

### Accelerometer_Trusted
This table contains only Accelerometer Readings from customers who agreed to share their data for research purposes. The script of the glue job is stored in:
- 02_trusted/accelerometer_landing_to_trusted.py

Query results are stored as:
- _screenshots/accelerometer_trusted.png
- _screenshots/accelerometer_trusted_count.png



## 5. Curated Zone
- tables
- customer
- machine learning