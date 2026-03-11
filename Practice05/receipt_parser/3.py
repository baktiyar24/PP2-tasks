import re
with open("raw.txt", "r", encoding='utf-8') as file:
    text = file.read()
Total = re.search(r'ИТОГО:\s*\n\s*([0-9 ]+,[0-9]{2})', text)
print(Total.group())