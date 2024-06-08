import numpy as np
import pandas as pd

from util import parsegpx
from matplotlib import pyplot as plt



gpxPath = 'data/Exercise.csv'
# parsedData = parsegpx(gpxPath)
df = pd.read_csv(gpxPath)

print(df.head(),'\n')

print(df.items())

exit()
print(f"Row count: {df.shape[0]} \n")
print(f"Column count: {df.shape[1]}")

# Getting familiar
df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)

plt.plot(df.Timestamp,df.Speed)
plt.xlabel('Timestamp')
plt.ylabel('Speed')
plt.title('Speed over time plot')
file_name = f"graphs/speedOverTime.png"
plt.savefig(file_name)

plt.clf()

plt.plot(df.Timestamp,df.hAcc)
plt.xlabel('Timestamp')
plt.ylabel('hAcc')
plt.title('hAcc over time plot')
file_name = f"graphs/hAccOverTime.png"
plt.savefig(file_name)

plt.clf()

plt.plot(df.Timestamp,df.Course)
plt.xlabel('Timestamp')
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