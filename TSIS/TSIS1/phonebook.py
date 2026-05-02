import json
import os
import sys

sys.path.append("TSIS/TSIS1")

from connect import get_connection

PAGE_SIZE = 5

# ---------------- DB ----------------

def fetch(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    data = cur.fetchall()
    conn.close()
    return data


def execute(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    conn.close()

# ---------------- FEATURES ----------------

def search_contacts(q):
    return fetch("SELECT * FROM search_contacts(%s::text)", (q,))


def filter_by_group(group):
    return fetch("""
        SELECT c.name, c.email, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))


def sort_contacts(opt):
    col = {"name":"name","birthday":"birthday","date":"created_at"}.get(opt,"name")
    return fetch(f"SELECT * FROM contacts ORDER BY {col}")


def paginate(offset):
    return fetch("""
        SELECT * FROM contacts
        ORDER BY id
        LIMIT %s OFFSET %s
    """, (PAGE_SIZE, offset))

# ---------------- JSON ----------------

def export_json():
    data = fetch("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    result = {}

    for name, email, birthday, group, phone, ptype in data:
        if name not in result:
            result[name] = {
                "name": name,
                "email": email,
                "birthday": str(birthday),
                "group": group,
                "phones": []
            }

        if phone:
            result[name]["phones"].append({
                "number": phone,
                "type": ptype
            })

    with open("contacts.json", "w") as f:
        json.dump(list(result.values()), f, indent=4)


def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:
        exist = fetch("SELECT id FROM contacts WHERE name=%s",(c["name"],))

        if exist:
            choice = input(f"{c['name']} exists (y overwrite / n skip): ")
            if choice.lower() != "y":
                continue

            execute("DELETE FROM contacts WHERE name=%s",(c["name"],))

        execute("""
            INSERT INTO contacts(name,email,birthday)
            VALUES (%s,%s,%s)
        """,(c["name"],c["email"],c["birthday"]))

        if c.get("group"):
            execute("CALL move_to_group(%s::text,%s::text)",
                    (c["name"],c["group"]))

        for p in c.get("phones", []):
            execute("CALL add_phone(%s::text,%s::text,%s::text)",
                    (c["name"],p["number"],p["type"]))

# ---------------- CSV ----------------

def import_csv():
    import csv
    with open("contacts.csv") as f:
        reader = csv.DictReader(f)

        for r in reader:
            execute("""
                INSERT INTO contacts(name,email,birthday)
                VALUES (%s,%s,%s)
            """,(r["name"],r["email"],r["birthday"]))

            execute("CALL move_to_group(%s::text,%s::text)",
                    (r["name"],r["group"]))

            execute("CALL add_phone(%s::text,%s::text,%s::text)",
                    (r["name"],r["phone"],r["type"]))

# ---------------- UTIL ----------------

def clear():
    os.system("cls" if os.name=="nt" else "clear")


def pagination_loop():
    offset = 0
    while True:
        clear()
        print(fetch("SELECT * FROM contacts ORDER BY id LIMIT %s OFFSET %s",(PAGE_SIZE,offset)))

        cmd = input("[n]next [p]prev [q]quit: ")

        if cmd=="n":
            offset += PAGE_SIZE
        elif cmd=="p":
            offset = max(0,offset-PAGE_SIZE)
        elif cmd=="q":
            break

# ---------------- MENU ----------------

def menu():
    while True:
        clear()
        print("""
========== PHONEBOOK ==========
1. Search contacts
2. Filter by group
3. Sort contacts
4. Pagination
------------------------------
5. Add phone
6. Move to group
------------------------------
7. Export JSON
8. Import JSON
9. Import CSV
0. Exit
==============================
""")

        c = input("Select: ")

        if c=="1":
            print(search_contacts(input("Search: ")))
            input()

        elif c=="2":
            print(filter_by_group(input("Group: ")))
            input()

        elif c=="3":
            print(sort_contacts(input("name/birthday/date: ")))
            input()

        elif c=="4":
            pagination_loop()

        elif c=="5":
            execute("CALL add_phone(%s::text,%s::text,%s::text)",
                    (input("Name: "),input("Phone: "),input("Type: ")))
            input("OK")

        elif c=="6":
            execute("CALL move_to_group(%s::text,%s::text)",
                    (input("Name: "),input("Group: ")))
            input("OK")

        elif c=="7":
            export_json()
            input("Exported")

        elif c=="8":
            import_json()
            input("Imported")

        elif c=="9":
            import_csv()
            input("CSV done")

        elif c=="0":
            break


if __name__=="__main__":
    menu()