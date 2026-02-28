from datetime import datetime, timedelta
import sys
import calendar

def parse(line):
    d, tz = line.strip().split()
    dt = datetime.strptime(d, "%Y-%m-%d")
    sign = 1 if tz[3] == '+' else -1
    h, m = map(int, tz[4:].split(':'))
    offset = timedelta(hours=h, minutes=m)
    return dt - sign * offset, dt.month, dt.day

birth_utc, bm, bd = parse(sys.stdin.readline())
current_utc, _, _ = parse(sys.stdin.readline())

def birthday_utc(year):
    day = bd
    if bm == 2 and bd == 29 and not calendar.isleap(year):
        day = 28
    local = datetime(year, bm, day)
    offset = birth_utc - datetime(birth_utc.year, bm if not (bm == 2 and bd == 29 and not calendar.isleap(birth_utc.year)) else 2, bd if not (bm == 2 and bd == 29 and not calendar.isleap(birth_utc.year)) else 28)
    return local - offset

year = current_utc.year
next_bday = birthday_utc(year)

if next_bday < current_utc:
    next_bday = birthday_utc(year + 1)

diff = (next_bday - current_utc).total_seconds()
print(int(diff // 86400) if diff > 0 else 0)