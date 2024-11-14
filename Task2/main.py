import csv 

with open('task-2-adjacency_matrix.csv') as f:
    graph = {line[0]:line[1:] for line in csv.reader(f)}

print(graph)


