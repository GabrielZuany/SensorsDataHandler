# Sensors Data Handler

This project presents the Sensors Data Handler, which aims to build a model capable of assessing and predicting possible failures and abnormalities in industrial equipment based on data collected from sensors. This document provides an overview of the project and is organized into chapters as follows:

---

## 1. Introduction

The Sensors Data Handler project focuses on developing a model to assess and predict potential failures and abnormalities in industrial equipment in real-time, leveraging data collected from sensors. The document is structured as follows:

- **Chapter 2: Data Reading**
- **Chapter 3: Data Preprocessing, Filtering, and Cleaning**
- **Chapter 4: Exploratory Analysis**
- **Chapter 5: Machine Learning Model**
- **Chapter 6: Real-world Scenario with Apache Kafka**

## 2. Data Reading

This chapter covers the data reading stage and techniques used in the development process.

### 2.1 Data Source

The data was provided in CSV format, with each sensor monitoring the equipment having a file of records.

### 2.2 Aggregation of Sensor Data

Two alternatives were considered for aggregating individual data into a single DataFrame: dynamic aggregation at runtime and pre-building a complete dataset. A script was created to construct the complete file if not found.

## 3. Data Preprocessing, Filtering, and Cleaning

This stage involves methods such as `head()`, `tail()`, `summarize()`, etc., to gain insights into the data. Duplicate rows were removed, and rows with all null values were cautiously eliminated. The DataFrame was reindexed with the timestamp column as the index, transforming it into a time series. Sorting based on the index was performed for better confidence in working with the data.

## 4. Exploratory Analysis

### 4.1 Initial Checks

Initial checks included examining the proportion of normal and abnormal states of the equipment within the recorded values to understand the predominant behavior.

### 4.2 Identification of Outliers

An analytical outlier identification method was applied due to the quantity of available data. The method proved accurate for the current case.

### 4.3 Correlation Between Variables (Sensors)

This step is essential for selecting the machine learning model. The correlation between sensor variables and the target (status) was analyzed. The results indicate predominantly independent sensors, leading to a multivariate analysis with independent features.

For detailed information, refer to the corresponding chapters in this document.

# Simulating Real Scenario with Apache Kafka

The Apache Kafka simulation within the Sensors Data Handler project allows for real-time data processing in an environment where sensor data is generated and consumed in real-time. The implementation uses Apache Kafka, an open-source stream processing platform developed by the Apache Software Foundation.

## 6. Simulating Real Scenario with Apache Kafka

### 6.1 Pipeline Architecture

The primary concept involves processing sensor data at each timestamp, formatting it, and writing it to the Kafka queue (producer). Subsequently, the consumer listens to this queue, reads, processes, and writes new records to the PostgreSQL database. The machine learning model script is then triggered, consuming from the table and generating real-time updated analyses.

### 6.2 Overview of Kafka

#### 6.2.1 Kafka Topic

Kafka "topics" store the sequence of received events and can be replicated across different partitions of the broker. For this project, a single topic (`SensorDataStream`) with two partitions was created.

#### 6.2.2 Enqueuing Data

Sensor data is read from the local file `full.csv` and inserted row by row into the Kafka queue with a 1-second delay to simulate real conditions.

#### 6.2.3 Processing the Queue

While messages are enqueued by the producer, the consumer processes them one by one, inserting them into the database and reading, processing, and formatting entries.

### 6.3 Database

PostgreSQL, running in Docker, was chosen as the database. The implementation is simple, focusing on values emitted by the sensors.

### 6.4 Real-time Algorithm

As values are generated in real-time, the Naive Bayes model is executed each time new data is inserted into the database, thereby increasing its accuracy.


## Running the Project Locally

To run the project on your machine, follow these steps:

1. Set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Install necessary dependencies in WSL:

```bash
sudo apt update
sudo apt upgrade
sudo apt install dos2unix
sudo apt install gnome-terminal
```

3. Execute the setup.sh script:

```bash
chmod +x kafka/setup.sh
chmod +x setup.sh
./setup.sh
```

---

- _More details in Docs/documentation_en_US.pdf or Docs/documentacao_pt_br.pdf_
