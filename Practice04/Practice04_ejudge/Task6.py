def fibonaci(n):
    a = 0 
    b = 1 
    for _ in range(n):
        yield a
        a, b = b, a+b

        
ob = int(input())
print(",".join(map(str, fibonaci(ob))))

