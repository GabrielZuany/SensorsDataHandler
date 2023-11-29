# Used to simulate the prediction of a Machine Learning model in real time
# Every second, the script makes a query in the database and checks if there is new data
# If so, it concatenates with the previous data and makes the prediction based on the new data set
# The model used is Naive Bayes, which is a simple and fast classification model

import time
import pandas as pd
import numpy as np
import psycopg2 as pg
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
    
TABLE_NAME = 'SensorsDataStream'

try:
    conn = pg.connect("dbname='postgres' user='postgres' host='localhost' password='example'")
    print("Connected to the database")
except Exception as e:
    print(e)
    exit(1)
    
def filter_df(df:pd.DataFrame):
    # Data cleaning
    # Drop duplicates and NaNs (when all rows/columns are NaN)
    df = df.drop_duplicates()
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    df = df.reset_index()

    df = df.reset_index()
    df = df.set_index('timestamp') if 'timestamp' in df.columns and df.index.name != "timestamp" else df
    df = df.sort_index()
    
    # drop the columns that are not useful
    try:
        df = df.drop(columns=['index'])
        df = df.drop(columns=['level_0'])   
    except:
        pass
       
    return df
    
cursor = conn.cursor()
full_df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
full_df = filter_df(full_df)
last_key = full_df.index[-1]

while True:
    query = f"SELECT * FROM {TABLE_NAME} WHERE {TABLE_NAME}.timestamp > '{last_key}'"
    tmp_df = pd.read_sql_query(query, conn)
    if tmp_df.empty:
        print("No new data")
        time.sleep(1)
        continue
    tmp_df = filter_df(tmp_df)
    full_df = filter_df(full_df)
    full_df = pd.concat([full_df, tmp_df], ignore_index=False, sort=True)
    full_df = filter_df(full_df)
    
    last_key = full_df.index[-1]
    print(f"Last timestamp: {last_key}")
    print(full_df)
    time.sleep(1)

    # set nan values to 0. The missing values might not affect the model
    full_df = full_df.fillna(0)

    # create a list of features
    features = full_df.columns.tolist()
    features.remove('status')

    # create a list of target
    target = 'status'

    # split the data into train and test
    X_train, X_test, y_train, y_test = train_test_split(full_df[features], full_df[target], test_size=0.2, random_state=42)

    # create a Gaussian and Bernoulli Naive Bayes classifier
    gnb = GaussianNB()
    bnb = BernoulliNB()

    # train the model using the training sets
    gnb.fit(X_train, y_train)
    bnb.fit(X_train, y_train)

    # predict the response for test dataset
    y_pred_gnb = gnb.predict(X_test)
    y_pred_bnb = bnb.predict(X_test)

    print(f"\nGNB accuracy: {accuracy_score(y_test, y_pred_gnb)}")
    print(f"\nBNB accuracy: {accuracy_score(y_test, y_pred_bnb)}")

    # check how many predictions match between the two models
    print(f"\nNumber of matching predictions: {np.sum(y_pred_gnb == y_pred_bnb)} / {len(y_pred_gnb)}")
    
    # next prediction status 
    print(f"\nNext prediction status GNB: {gnb.predict(full_df[features].iloc[[-1]])}")
    print(f"\nNext prediction status BNB: {bnb.predict(full_df[features].iloc[[-1]])}")
    print(f"Number of ANORMAL status find until now: {len(full_df[full_df['status'] == 'ANORMAL'])}")
    
    print("========================================")