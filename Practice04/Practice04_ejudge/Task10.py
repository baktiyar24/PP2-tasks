def numbers(lst, times):
    for _ in range(times):
        for value in lst:
            yield value

lst = input().split()
times = int(input())
for x in numbers(lst, times):
    print(x, end=" ")

