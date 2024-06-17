import os
import numpy as np
import pandas as pd

from numpy import sqrt
from datetime import datetime, timedelta
from matplotlib import pyplot as plt


directory = "phoneData"
fileList = ['Accelerometer.csv', 'Gyroscope.csv']


for folder in os.listdir(directory):
    metaDf = pd.read_csv(f'{directory}/{folder}/meta/time.csv')
    for fileName in fileList:
        # parsedData = parsegpx(gpxPath)
        df = pd.read_csv(f'{directory}/{folder}/{fileName}')

        shortenedFileName = fileName[:3].lower()
        df = df.rename(columns={"Time (s)": "timestamp",
                                 f'{df.columns[1]}': f"{shortenedFileName}_{df.columns[1][:1].lower()}", 
                                 f'{df.columns[2]}': f"{shortenedFileName}_{df.columns[2][:1].lower()}", 
                                 f'{df.columns[3]}': f"{shortenedFileName}_{df.columns[3][:1].lower()}"})

        print(df.head())

        df[f"absolute"] = sqrt(df[f'{shortenedFileName}_x']**2+df[f'{shortenedFileName}_y']**2+df[f'{shortenedFileName}_z']**2)

        start_timestamp = metaDf['system time'][1]
        df['timestamp'] = df.apply(lambda row: datetime.fromtimestamp(start_timestamp+row.timestamp), axis=1)
        df.timestamp = pd.to_datetime(df.timestamp)

        df.to_csv(f'{directory}/{folder}/{fileName[:3]}_out.csv', index=False)

for folder in os.listdir(directory):
    df_gyr = pd.read_csv(f'{directory}/{folder}/Gyr_out.csv')
    df_gyr.timestamp = pd.to_datetime(df_gyr.timestamp)
    df_acc = pd.read_csv(f'{directory}/{folder}/Acc_out.csv')
    df_acc.timestamp = pd.to_datetime(df_acc.timestamp)
    df =  pd.merge_asof(df_gyr, df_acc, on='timestamp')

    df['label'] = folder

    df.to_csv(f'{directory}/{folder}/merged_out.csv', index=False)

dfFinal = pd.DataFrame()
for folder in os.listdir(directory):
    df = pd.read_csv(f'{directory}/{folder}/merged_out.csv')
    dfFinal = pd.concat([dfFinal, df])

dfFinal.to_csv(f'{directory}/new_out.csv', index=False)

df = pd.read_csv(f'{directory}/new_out.csv')

def timeGeneration():
    global startTime
    startTime+=0.1
    return startTime

startTime = 1.718541388418760E9
df['timestamp'] = df.apply(lambda row: datetime.fromtimestamp(timeGeneration()), axis=1)

print(df.head())

df.to_csv(f'test_out.csv', index=False)
