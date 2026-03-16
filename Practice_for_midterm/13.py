import re
import json
d = json.loads(input())
for name, price in d.items():
    if re.match(r"\$\d{2,1000000}.\d+", price):
        print(name)