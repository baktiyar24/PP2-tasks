n = int(input())
nums = list(map(int, input().split()))
for i in range(len(nums)):
    nums[i] = pow(nums[i], 2)
print(*nums)
