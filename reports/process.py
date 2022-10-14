import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import csv

x = []
y = []
with open('users.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x.append(row[0])
        y.append(row[1])
#  polynomial order 1/2 of length (approx)
yhat = savgol_filter(y, len(x) -1, 2) 


plt.plot(x,y)
plt.plot(x,yhat, color='red')
plt.show()

# values = list(zip(x_arr, y_arr))
# print(values)