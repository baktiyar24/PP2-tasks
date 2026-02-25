def evens(n):
    for i in range(0, n+1, 2):
        yield i

n = int(input())
result = ",".join(str(x) for x in evens(n))
print(result)

