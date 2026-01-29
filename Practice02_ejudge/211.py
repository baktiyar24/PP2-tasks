n, l, r = map(int, input().split())
nums = list(map(int, input().split()))
l -= 1
r -= 1
part = nums[l:r+1]
part.reverse()          
nums[l:r+1] = part
print(*nums)
