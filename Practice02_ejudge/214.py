n = int(input())
a = list(map(int, input().split()))

max_count = 0
answer = a[0]

for x in a:
    count = 0
    for y in a:
        if y == x:
            count += 1

    if count > max_count or (count == max_count and x < answer):
        max_count = count
        answer = x

print(answer)