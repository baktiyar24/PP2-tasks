import datetime 
today = datetime.date.today()
after_time = datetime.timedelta(days=5) + today
print(today)
print(after_time)