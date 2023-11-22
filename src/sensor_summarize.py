import os
import pandas as pd

# parallel processing 
# make a model for each tag and run them in parallel to summarize the data

DATAFOLDER = 'data/'
BASE_NAME = 'TAG_iALL_PS_'

data_00 = pd.read_csv(DATAFOLDER + 'TAG_iALL_PS_00.csv')
data_00 = data_00.set_index('timestamp')

print(data_00.head())
print(data_00.shape)
print(data_00.columns)
print(data_00.describe())

# full_df = pd.DataFrame()
# for file in os.listdir(DATAFOLDER):
#     if file.startswith(BASE_NAME):
#         # print(file)
#         df = pd.read_csv(DATAFOLDER + file)
#         full_df = pd.concat([full_df, df], ignore_index=True)
# print(full_df.head())

