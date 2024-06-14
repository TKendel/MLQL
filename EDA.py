import numpy as np
import pandas as pd

from numpy import sqrt
from datetime import datetime, timedelta
from matplotlib import pyplot as plt


file_paths = ['Gyroscope.csv', 'Accelerometer.csv']
for file in file_paths:
    # parsedData = parsegpx(gpxPath)
    df = pd.read_csv(f'data/{file}')

    shortened_column_name = df.columns[1][:3].lower()
    df = df.rename(columns={"Time (s)": "timestamp", f'{df.columns[1]}': f"{shortened_column_name}_x", f'{df.columns[2]}': f"{shortened_column_name}_y", f'{df.columns[3]}': f"{shortened_column_name}_z"})

    df[f"absolute_{shortened_column_name}"] = sqrt(df[f'{shortened_column_name}_x']**2+df[f'{shortened_column_name}_y']**2+df[f'{shortened_column_name}_z']**2)

    start_timestamp = 1718265622.307
    df['timestamp'] = df.apply(lambda row: datetime.fromtimestamp(start_timestamp+row.timestamp), axis=1)
    df.timestamp = pd.to_datetime(df.timestamp)
    # df['timestamp'] = pd.to_datetime(df['timestamp'],format).apply(lambda x: x.time())

    print(df.head())

    df.to_csv(f'{shortened_column_name}_out.csv', index=False)

df_gyr = pd.read_csv('gyr_out.csv')
df_gyr.timestamp = pd.to_datetime(df_gyr.timestamp)
df_acc = pd.read_csv('acc_out.csv')
df_acc.timestamp = pd.to_datetime(df_acc.timestamp)

print(df_acc.timestamp.dtype)

df =  pd.merge_asof(df_gyr, df_acc, on='timestamp')

print(df.head())

df.to_csv('merged_out.csv', index=False)

exit()
print(f"Row count: {df.shape[0]} \n")
print(f"Column count: {df.shape[1]}")

# # Getting familiar
# df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)

plt.plot(df.timestamp,df.absolute_acc)
plt.xlabel('timestamp')
plt.ylabel('Speed')
plt.title('Speed over time plot')
file_name = f"graphs/speedOverTime.png"
plt.savefig(file_name)

plt.clf()

exit()

plt.plot(df.Timestamp,df.hAcc)
plt.xlabel('timestamp')
plt.ylabel('hAcc')
plt.title('hAcc over time plot')
file_name = f"graphs/hAccOverTime.png"
plt.savefig(file_name)

plt.clf()

plt.plot(df.Timestamp,df.Course)
plt.xlabel('timestamp')
plt.ylabel('Course')
plt.title('Course over time plot')
file_name = f"graphs/courseOverTime.png"
plt.savefig(file_name)

plt.clf()

## Add velocity from xyz
# for i in range(0, len(dT)):
# 	# print(aX[i])
# 	# print(dT[i])
# 	# print(f"{aX[i]}, {aY[i]}, {aZ[i]}")
# 	print(f"{aX[i]+aY[i]+aZ[i]+0.980665}")
# 	uX += aX[i]*(dT[i]/1000)
# 	uY += aY[i]*(dT[i]/1000)
# 	uZ += aZ[i]*(dT[i]/1000)
# 	vX.append(uX)
# 	vY.append(uY)
# 	vZ.append(uZ)
# 	velocity.append(uX+uY+uZ)
# 	# print(f"{uX}, {uY}, {uZ}")