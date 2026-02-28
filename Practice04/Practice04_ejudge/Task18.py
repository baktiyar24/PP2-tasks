x0, y0 = map(float, input().split())
x1, y1 = map(float, input().split())

xr = (x0 * y1 + x1 * y0) / (y0 + y1)
yr = 0.0

print(f"{xr:.10f} {yr:.10f}")