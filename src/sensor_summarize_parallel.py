from multiprocessing import cpu_count
import os
import time
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

DATAFOLDER = 'data/'
BASE_NAME = 'TAG_iALL_PS_'

start_time = time.time()

def read(file):
    if file.endswith('00.csv'):
        return None

    print('Reading file: ' + file)
    df = pd.read_csv(DATAFOLDER + file)
    df = df.set_index('timestamp')

    return df[file.split('.')[0]]

if __name__ == '__main__':
    # Get the list of files to process
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