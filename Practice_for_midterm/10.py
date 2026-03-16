import re
data = input()
d = re.findall(r"\d+", data)
for n in d:
    print(n)