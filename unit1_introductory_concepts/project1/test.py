import itertools
import random
arr = [[2,3],[5,3],[4,3]]
x = random.choice(arr)
print(x)

def hoge(x):
  print("hoge")
  if x > 3:
    return 1,2,False
  else:
    return 1,2

x = hoge(2)
# print(x)
arr=list(itertools.product(range(9),range(9)))
print(itertools.product(range(9),range(9)))

# for i in range(9):
#   for j in range(9):

data = []

for i, j in itertools.product(range(9),range(9)):
  if j==0:
    data.append([])
  if i==0:
    data[i].append("X")
  elif i==8:
    data[i].append("Y")
  else:
    data[i].append(" ")

print(data)

