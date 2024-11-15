# Подготовка к запуску и Quick Start

В директорию, где хранится .py файл, следует сохранить исходный CSV файл с названием 'task1.csv'. Для дальнейших действий обратиться к [Quick Start инструкции](https://github.com/Quantum-Beavers/QuantHackaton_2024/blob/master/Task1/QuickStartGuide.md).

# Сегмент кода

## Импорт библиотек

```python
from time import time
import numpy as np
from scipy.sparse import coo_matrix
import pyqiopt as pq
import csv 
from math import sqrt
```

## Чтение входных данных из файла

```python
with open('./ArtTesting/task1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    pi = []
    title = False
    for row in spamreader:
        if title:

            pi.append(list(map(float,row)))

        title = True
```

## Вычисление и заполнение матрицы исходных элементов
```python
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
```

## Инициализация необходимых для конвертации в coo_matrix переменных

```python
row = np.array([])
column = np.array([])
data = np.array([])
R = 0.2
q1 = 1 
q2 = 20
```


## Заполнение матрицы QUBO согласно заранее выработанным формулам

```python
for i in range(100):
    for j in range(100):
        row = np.hstack((row,[i]))
        column = np.hstack((column,[j]))
        if (i == j):
            data = np.hstack((data,[q2*r[i]**2 - q2*2*r[i]*R - q1*p[i]]))
        else:
            data = np.hstack((data,[q2*r[i]*r[j]]))
```

## Конвертация в coo_matrix для дальнейшей работы с solve

```python
sparse_matrix = coo_matrix((data, (row, column)), shape=(100,100))

arr = sparse_matrix.todense()
```

## Фиксируем время старта решения

```python
start = time()
```

## Запуск и сохранение solve

```python
arr_sp = coo_matrix(arr)

sol = pq.solve(arr_sp, number_of_runs=10, number_of_steps=100, return_samples=False, verbose=10)
```

## Вывод купленных акций

```python
print("Портфель акций содержит в себе следующие акции, имеющиее соответственно среднуюю за период доходность и риск:")
for i in range(len(sol.vector)):
  if sol.vector[i] == 1:
    print(f"Акция s{i}, доход {p[i]}, риск {r[i]}")
```

## Заполнение массива доходности и риска для выбранных акций

```python
sr = 0
sp = 0

for i in range(n-1):
  if (sol.vector[i]):
    sr +=r[i]
    sp+=p[i]
```

# Вывод общего дохода и риска с выбранных акций

```python
print(f"Общие доход и риск равны соответственно: {sp}, {sr} ")
```

# Вывод времени затраченного на решение данной задачи

```python
print("Script time:", time()-start)
```
