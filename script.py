from runtime import *
import numpy as np
import csv
regret_arr = []
regret_ar = []
a = 100
fairness_arr = []
len_fairness = 0
result_fairness = []
temp_fairness = []
fairness_ar = []
result_fairness = []

for i in range(a):
    # debug = input("print or not/1 or 0")
    debug = 0
    regret_arr, fairness_arr, time = call(debug)
    regret_ar.append(regret_arr)

    for i in range(len(fairness_arr)):
        result_fairness.append(fairness_arr[i])

# print(result_fairness)
regret_a = [0]*len(regret_arr)

result_f = [[0]*len(fairness_arr[0])for i in range(len(fairness_arr))]

for i in range(len(result_fairness)):
    for j in range(len(fairness_arr[0])):
        result_f[i % 6][j] += result_fairness[i][j]


for j in range(len(result_f)):
    for i in range(len(result_f[0])):
        result_f[j][i] = result_f[j][i]/a

for i in range(a):
    for j in range(len(regret_arr)):
        regret_a[j] += regret_ar[i][j]
for i in range(len(regret_arr)):
    regret_a[i] = regret_a[i]/a
#print("regret_avg_array", regret_a)
#print("fairness_avg_array", result_f)

plt.scatter(time, regret_a)
plt.xlabel("Time(Rounds)")
plt.ylabel("Time-average regret")
plt.ylim(-0.2, 1)
plt.show()

plt.scatter([math.log(i) for i in time], [math.log(i)for i in regret_a])
plt.ylim(-7.0, 10)
plt.xlabel("logT")
plt.ylabel("log(Time-average regret)")
plt.show()

color = ['r.', 'g.', 'b.', 'k.', 'y.', 'm.']
label = ['Arm 1', 'Arm 2', 'Arm 3', 'Arm 4', 'Arm 5', 'Arm 6']
for i in range(6):
    plt.plot(range(len(result_f[i])), result_f[i], color[i], label=label[i])
plt.ylim(0, 1)
plt.xlabel("Rounds")
plt.ylabel("Selection fraction")
plt.legend(loc='lower right')
plt.show()

with open("array.csv", 'w')as myarray:
    wr = csv.writer(myarray, delimiter=",")
    wr.writerow([result_f])
