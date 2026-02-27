n = int(input())
nums = list(map(int, input().split()))
b = max(nums)
index = 0
for i in range(n+1):
    if b == nums[i]:
        index = i +1
        break

print(index)

