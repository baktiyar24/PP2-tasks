import datetime
today = input()
date_today = datetime.datetime.strptime(today, "%Y-%m-%d").date()
future = date_today + datetime.timedelta(days=5)
print(future)