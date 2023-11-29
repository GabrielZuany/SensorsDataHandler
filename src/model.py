from multiprocessing import cpu_count
import os
import time
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import numpy as np

DATAFOLDER = '../data/'
BASE_NAME = 'TAG_iALL_PS_'
full_csv_exists = 'full.csv' in os.listdir(DATAFOLDER)

if full_csv_exists:
    start_time = time.time()
    full_df = pd.read_csv('../data/full.csv')
    end_time = time.time()
    print('Elapsed time: ' + str(end_time - start_time) + ' seconds')

else:
    start_time = time.time()
    def read(file):
        if file.endswith('00.csv'):
            return None

        print('Reading file: ' + file)
        df = pd.read_csv(DATAFOLDER + file)
        df = df.set_index('timestamp')

        return df[file.split('.')[0]]

    files_to_process = [file for file in os.listdir(DATAFOLDER) if not file.endswith('00.csv')]

    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor(cpu_count()) as executor:
        # Map the function to process each file in parallel
        dfs = list(executor.map(read, files_to_process))

    # Create the full_df by concatenating the DataFrames
    full_df = pd.concat([pd.read_csv(DATAFOLDER + 'TAG_iALL_PS_00.csv').set_index('timestamp')] + dfs, ignore_index=False, axis=1)

    # Rename the 'target_iALL_PS' column to 'status' 
    if 'target_iALL_PS.csv' in files_to_process:
        full_df = full_df.rename(columns={'target_iALL_PS': 'status'})

    # Save the result to a CSV file
    full_df.to_csv(DATAFOLDER + 'full.csv')
    end_time = time.time()
    print('Elapsed time: ' + str(end_time - start_time) + ' seconds')
    


# Data cleaning
# Drop duplicates and NaNs (when all rows/columns are NaN)
full_df = full_df.drop_duplicates()
full_df = full_df.dropna(axis=1, how='all')
full_df = full_df.dropna(axis=0, how='all')
full_df = full_df.reset_index()

# Convert the timestamp column to datetime and set it as the index
full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])
full_df = full_df.sort_values(by='timestamp')
full_df = full_df.reset_index()
full_df = full_df.set_index('timestamp') if 'timestamp' in full_df.columns else full_df

# Create a column with the status as a boolean (might be useful for plotting later)
full_df['status_bool'] = np.where(full_df['status'] == 'NORMAL', 0, 1)

# drop the columns that are not useful
full_df = full_df.drop(columns=['index'])
full_df = full_df.drop(columns=['level_0'])


from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# set nan values to 0. The missing values might not affect the model
full_df = full_df.fillna(0)

# create a list of features
features = full_df.columns.tolist()
features.remove('status')
features.remove('status_bool')

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

# print the first 10 anormal predictions
def print_result_sample(y_pred, y_test):
    first_10_anormal_predictions = []
    first_10_anormal_actual = []
    for i in range(len(y_pred)):
        if y_pred[i] == 'ANORMAL':
            first_10_anormal_predictions.append(y_pred[i])
            first_10_anormal_actual.append(y_test[i])
            if len(first_10_anormal_predictions) == 10:
                break

    print(first_10_anormal_predictions)
    print(first_10_anormal_actual)

print(f"\nGNB accuracy: {accuracy_score(y_test, y_pred_gnb)}")
print_result_sample(y_pred_gnb, y_test)
print(f"\nBNB accuracy: {accuracy_score(y_test, y_pred_bnb)}")
print_result_sample(y_pred_bnb, y_test)

# check how many predictions match between the two models
print(f"\nNumber of matching predictions: {np.sum(y_pred_gnb == y_pred_bnb)} / {len(y_pred_gnb)}")