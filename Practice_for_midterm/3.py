from datetime import *
date1 = input()
date2 = input()
dates1 = datetime.strptime(date1, "%Y-%m-%d")
dates2 = datetime.strptime(date2, "%Y-%m-%d")
data = abs(dates1 - dates2).days
print(data)