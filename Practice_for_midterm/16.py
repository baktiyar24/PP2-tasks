import math
import cmath
x, y = map(int, input().split())
c = math.atan2(y,x)
print(math.degrees(c))