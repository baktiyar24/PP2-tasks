from datetime import datetime, timedelta
import sys

def parse(s):
    date, time, tz = s.strip().split()
    dt = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
    sign = 1 if tz[3] == '+' else -1
    h, m = map(int, tz[4:].split(':'))
    return dt - sign * timedelta(hours=h, minutes=m)

start = parse(sys.stdin.readline())
end = parse(sys.stdin.readline())

print(int((end - start).total_seconds()))