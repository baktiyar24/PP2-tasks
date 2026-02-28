import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx, dy = x2 - x1, y2 - y1
a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - r*r
disc = b*b - 4*a*c

if disc <= 0:
    print("0.0000000000")
else:
    t1 = (-b - math.sqrt(disc)) / (2*a)
    t2 = (-b + math.sqrt(disc)) / (2*a)
    t1 = max(0, min(1, t1))
    t2 = max(0, min(1, t2))
    length = math.hypot(dx, dy) * max(0, t2 - t1)
    print(f"{length:.10f}")