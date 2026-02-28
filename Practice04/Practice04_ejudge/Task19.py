import math

r = float(input())
x0, y0 = map(float, input().split())
x1, y1 = map(float, input().split())

d0 = math.hypot(x0, y0)
d1 = math.hypot(x1, y1)
c = math.hypot(x1 - x0, y1 - y0)

if d0 >= r and d1 >= r:
   
    dx, dy = x1 - x0, y1 - y0
    t = -(x0*dx + y0*dy) / (dx*dx + dy*dy)
    closest_x = x0 + t*dx
    closest_y = y0 + t*dy
    if t >= 0 and t <= 1 and math.hypot(closest_x, closest_y) < r:
       
        alpha0 = math.acos(r/d0)
        alpha1 = math.acos(r/d1)
        theta = math.atan2(y1, x1) - math.atan2(y0, x0)
        theta = abs(theta)
        arc = r * (theta - alpha0 - alpha1)
        length = math.sqrt(d0*d0 - r*r) + math.sqrt(d1*d1 - r*r) + arc
        print(f"{length:.10f}")
    else:
        print(f"{c:.10f}")
else:
    print(f"{c:.10f}")