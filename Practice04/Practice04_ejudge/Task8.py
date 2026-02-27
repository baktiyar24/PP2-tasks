def is_prime(num):
    if num <= 1:
        return False 
    for i in range(2, num):
        if num % i == 0:
            return False
        
    return True

def prime_num(n):
    for num in range(1, n+1):
        if is_prime(num):
            yield num

n = int(input())
ob = prime_num(n)
for x in ob:
    print(x, end=" ")