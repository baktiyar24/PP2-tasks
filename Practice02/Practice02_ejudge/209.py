n = int(input())
nums = list(map(int, input().split()))
minimal = min(nums)
maximal = max(nums)
new_nums = []
for x in nums:

    if x == maximal:
        x = minimal
    print(x, end=" ")


