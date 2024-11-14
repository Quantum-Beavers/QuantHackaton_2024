from time import time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse import random
from scipy import stats
import pyqiopt as pq
import csv 
from math import sqrt

with open('task1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    pi = []
    title = False
    for row in spamreader:
        if title:

            pi.append(list(map(float,row)))

        title = True
    

n = len(pi) - 1 

p = []
for i in range(len(pi[0])):
    s = 0
    for j in range(1, n):
        s += (pi[j + 1][i] - pi[j][i])/pi[j][i]
    s/=n-1
    
    p.append(s)

r = []
for i in range(len(pi[0])):
    s = 0
    for j in range(1, n):
        s += ((pi[j + 1][i] - pi[j][i])/pi[j][i] - p[i])**2

    s=sqrt(s*n/(n-1))
    
    r.append(s)


row = np.array([])
column = np.array([])
data = np.array([])
R = 0.2
q1 = 1 
q2 = 20

for i in range(100):
    for j in range(100):
        row = np.hstack((row,[i]))
        column = np.hstack((column,[j]))
        if (i == j):
            data = np.hstack((data,[q2*r[i]**2 - q2*2*r[i]*R - q1*p[i]]))
        else:
            data = np.hstack((data,[q2*r[i]*r[j]]))
sparse_matrix = coo_matrix((data, (row, column)), shape=(100,100))

arr = sparse_matrix.todense()
print("Non zero elements:", np.count_nonzero(arr))
start = time()
print("Numpy matrix example")
sol = pq.solve(arr, number_of_runs=1, number_of_steps=51, return_samples=False, verbose=10)
print(sol.vector, sol.objective)
arr_sp = coo_matrix(arr) # for pyqiopt input use COO format only
print("Sparse COO matrix example")
sol = pq.solve(arr_sp, number_of_runs=1, number_of_steps=100, return_samples=False, verbose=10)
print(sol.vector, sol.objective)
sr = 0
sp = 0
for i in range(100):
  if (sol.vector[i]):
    sr +=r[i]
    sp+=p[i]
print(sr,sp)
print("Sampling example")

sol = pq.solve(arr_sp, seed = 2323,  number_of_runs=1, number_of_steps=100, return_samples=True, verbose=10)

print(sol.vector)
sr = 0
sp = 0

for i in range(100):
  if (sol.vector[i]):
    sr +=r[i]
    sp+=p[i]
print(sr,sp)
print(sol.samples)
print("Script time:", time()-start)