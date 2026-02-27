def powers(n):
    for i in range(0,n+1):
        yield 2**i

n = int(input())
for x in powers(n):
    print(x, end=" ")
