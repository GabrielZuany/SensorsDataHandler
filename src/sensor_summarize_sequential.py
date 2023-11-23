import os
import time
import pandas as pd

DATAFOLDER = 'data/'
BASE_NAME = 'TAG_iALL_PS_'

start_time = time.time()

TAG_iALL_PS_00 = pd.read_csv(DATAFOLDER + 'TAG_iALL_PS_00.csv')
TAG_iALL_PS_00 = TAG_iALL_PS_00.set_index('timestamp')

full_df = pd.DataFrame()
full_df = pd.concat([full_df, TAG_iALL_PS_00], ignore_index=False)
for file in os.listdir(DATAFOLDER):
    if file.endswith('00.csv'):
        continue
    print('Reading file: ' + file)
    df = pd.read_csv(DATAFOLDER + file)
    df = df.set_index('timestamp')
    full_df = pd.concat([full_df, df[file.split('.')[0]]], ignore_index=False, axis=1)
    if file == 'target_iALL_PS.csv':
        full_df = full_df.rename(columns={'target_iALL_PS': 'status'})
    
full_df.to_csv(DATAFOLDER + 'full.csv')
# print(full_df.head())

end_time = time.time()
print('Elapsed time: ' + str(end_time - start_time) + ' seconds')