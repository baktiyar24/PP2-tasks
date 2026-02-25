import json
with open("sample-data.json", "r") as file:
    data = json.load(file)


print("Interface Status")
print("==============================================\n")
print("DN                                           Description   Speed   MTU")
print("------------------------------------------- -------------- -------------")

    