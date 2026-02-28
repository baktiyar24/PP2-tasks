from datetime import datetime, timedelta
import sys

def parse(s):
    date_part, tz_part = s.strip().split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    sign = 1 if tz_part[3] == '+' else -1
    h, m = map(int, tz_part[4:].split(':'))
    offset = timedelta(hours=h, minutes=m)
    return dt - sign * offset

a = parse(sys.stdin.readline())
b = parse(sys.stdin.readline())

seconds = abs((a - b).total_seconds())
print(int(seconds // 86400))