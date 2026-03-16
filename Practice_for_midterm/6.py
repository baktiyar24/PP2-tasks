import re
d = input()
pattern = "Daniyar"
if re.match(pattern, d):
    print("Daniyar krasavchik")
else:
    print("daniyar mal")