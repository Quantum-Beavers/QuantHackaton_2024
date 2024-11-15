import csv
import numpy
from scipy import sparse
from time import time
# import pyqiopt as pq


TRANSPORT = 15
PEOPLE = 10

with open('task-2-adjacency_matrix.csv') as f:
    graph = {line[0]:line[1:] for line in csv.reader(f)}

with open('task-2-nodes.csv') as f:
    nodes = {line[0]:line[1:] for line in csv.reader(f)}

print(nodes)

startPoint = graph.get('Вокзал')
nameAllPoints = graph.get('\ufeff')

flag = 0
quboMatrix = numpy.array([])
for i in graph:
    if (flag == 0):
        flag = 1
        continue
    normArray = graph.get(i,[])
    for j in range(0, len(normArray)):
        if (normArray[j] == "-"):
            normArray[j] = "-1"
        normArray[j] = int(normArray[j])
    if (flag == 1):
        quboMatrix = numpy.array(normArray)
        flag = 2
        continue
    quboMatrix = numpy.vstack((quboMatrix, numpy.array(normArray)))

quboMatrixTriu = numpy.triu(quboMatrix)

quboMatrixSparse = sparse.coo_matrix(quboMatrix)

quboMatrixTriuSparse = sparse.coo_matrix(quboMatrixTriu)

start = time()

print("Non zero elements:", numpy.count_nonzero(quboMatrix))

# print("Numpy matrix example")
# sol = pq.solve(quboMatrixSparse, number_of_runs=1, number_of_steps=100, return_samples=False, verbose=10)
# print(sol.vector, sol.objective)
#
# print("Sparse COO matrix example")
# sol = pq.solve(quboMatrixSparse, number_of_runs=1, number_of_steps=100, return_samples=False, verbose=10)
# print(sol.vector, sol.objective)
#
# print("Sampling example")
# sol = pq.solve(quboMatrixSparse, number_of_runs=1, number_of_steps=100, return_samples=True, verbose=10)
# print(sol.samples)

# print("quboMatrix:")
# print(quboMatrix)
#
# print("quboMatrixTriu:")
# print(quboMatrixTriu)
#
# print("quboMatrixSparse:")
# print(quboMatrixSparse)
#
# print("quboMatrixTriuSparse:")
# print(quboMatrixTriuSparse)


print("Script time:", time()-start)
