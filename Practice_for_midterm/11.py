import re
import json
date = json.loads(input())
for name, numbers in date.items():
    if re.match(r"\d{3}-\d{3}-\d+", numbers):
        print(name)
        
