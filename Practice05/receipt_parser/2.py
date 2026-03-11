import re
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

names = re.findall(r"\d+\.\n(.+)",text)
print(names)