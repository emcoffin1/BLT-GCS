import random

l = {"1":1, "2":2, "3":3}
g = {"1":[1], "3":[2]}
w = 1
for i,j in l.items():
    if i in g.keys():
        g[i].append(4)


g["1"].pop(0)
# print(g)

for i, j in l.items():
    if i in g.keys():
        print(g[i])