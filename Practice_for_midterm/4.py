import datetime
date1 = input()
date2 = input()
dates1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
dates2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
timedeltas = abs(dates1 - dates2).total_seconds()
print(int(timedeltas))