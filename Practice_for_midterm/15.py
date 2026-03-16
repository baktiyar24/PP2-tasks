import math as m
x1, y1, x2, y2 = map(int, input().split())
print(m.sqrt((pow(x2-x1, 2)+pow(y2-y1, 2))))