import re
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()
prices = re.findall(r'Стоимость\s*\n\s*([0-9 ]+,[0-9]{2})', text)
print(prices)