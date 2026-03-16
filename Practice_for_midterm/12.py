import re
import json
d = json.loads(input())
for name, yahoo in d.items():
    if re.match(r"\S+@yahoo.com", yahoo):
        print(name)