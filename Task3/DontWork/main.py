import csv
import re
import numpy
import cirq
import sympy

data_sentence = []
data_ans = []
words = []

with open('task-3-dataset.csv', encoding="utf8") as f:
    reader = csv.reader(f)
    i = -1
    for row in reader:
        if i != -1:
            data_ans.append(int([1 if row[1] == "+" else 0][0]))
            data_sentence.append([])
            for word in re.split(r"[,.?!;)(:/\s]+", row[0]):
                if (word not in words and (len(word) > 2 or word.lower() == "не") and
                        word.lower() not in ("-", "qphone", "pro", "max") and not word.isnumeric()):
                    data_sentence[i].append(word.lower())
                    words.append(word.lower())
            i += 1
        else:
            i = 0
print(data_sentence)

WORDS_COUNT = len(words)
qubits = cirq.LineQubit.range(WORDS_COUNT)
x = sympy.symbols(f"x0:{WORDS_COUNT}")
thetas = sympy.symbols(f"t0:{WORDS_COUNT}")
circuit = cirq.Circuit()

for i in range(WORDS_COUNT):
    circuit.append(cirq.rx(x[i])(qubits[i]))
    circuit.append(cirq.ry(0)(qubits[i]))

# for i in circuit[0]:
#     print(i.qubits[0])
# for j in circuit[1]:
#     print(j.gate)
# print(circuit[1].operations[1].gate)


# for i in circuit[0].qubits:
#     print(i)

# circuit0 = cirq.Circuit(cirq.X.on(cirq.GridQubit(0, 1)))
# print(circuit0)
# # transforming the qubits
# qubit_map = {cirq.GridQubit(0, 1): cirq.GridQubit(5, 7)}
# circuit0 = circuit0.transform_qubits(qubit_map=qubit_map)
# print(circuit0)

REPETITIONS = 1
for _ in range(REPETITIONS):
    for i in range(len(data_sentence)):
        ans = 0.5
        for j in range(len(data_sentence[i])):
            ans += float(str(circuit[1].operations[words.index(data_sentence[i][j])].gate).split("Ry(")[1].split("π)")[0])
        print(ans)
        if data_ans[i] == 1:
            for j in range(len(data_sentence[i])):
                qubit_map = {circuit[1].operations[words.index(data_sentence[i][j])]: cirq.LineQubit(cirq.ry(
                    float(
                        str(circuit[1].operations[words.index(data_sentence[i][j])].gate).split("Ry(")[1].split("π)")[0]
                ) + 1))}
                circuit = circuit.transform_qubits(qubit_map=qubit_map)
        else:
            for j in range(len(data_sentence[i])):
                qubit_map = {circuit[1].operations[words.index(data_sentence[i][j])]: cirq.LineQubit(cirq.ry(
                    float(
                        str(circuit[1].operations[words.index(data_sentence[i][j])].gate).split("Ry(")[1].split("π)")[0]
                ) - 1))}
                circuit = circuit.transform_qubits(qubit_map=qubit_map)
    print(circuit)
