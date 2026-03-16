import datetime
date_str = input()
date = datetime.date.strptime(date_str, "%Y-%m-%d")
date_after = date + datetime.timedelta(days = 10)
print(date_after)