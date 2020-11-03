import pickle as pk

with open('list', 'rb') as f:
    li = pk.load(f)

print(li)
