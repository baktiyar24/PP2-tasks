import csv
import json
from datetime import date, datetime
from connect import get_connection


def _fmt_row(row):
    cid, username, email, birthday, group_name, phones_agg, created_at = row
    return (
        f"[{cid}] {username}"
        f" | email: {email or '—'}"
        f" | birthday: {birthday or '—'}"
        f" | group: {group_name or '—'}"
        f" | phones: {phones_agg or '—'}"
    )


def _input_date(prompt):
    while True:
        raw = input(prompt + " (YYYY-MM-DD or blank): ").strip()
        if not raw:
            return None
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Invalid date format")


def _pick_group(cur):
    cur.execute("SELECT id, name FROM groups ORDER BY id")
    groups = cur.fetchall()

    for gid, gname in groups:
        print(gid, gname)

    raw = input("group: ").strip()

    for gid, _ in groups:
        if str(gid) == raw:
            return gid
    return None


def insert_from_console():
    username = input("name: ").strip()
    email = input("email: ").strip() or None
    birthday = _input_date("birthday")

    conn = get_connection()
    cur = conn.cursor()

    group_id = _pick_group(cur)

    cur.execute(
        "INSERT INTO contacts (username, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
        (username, email, birthday, group_id)
    )

    contact_id = cur.fetchone()[0]

    while True:
        phone = input("phone: ").strip()
        if not phone:
            break
        ptype = input("type: ").strip() or "mobile"
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
            (contact_id, phone, ptype)
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv(filename="contacts.csv"):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            username = row.get("username")
            email = row.get("email") or None
            birthday = row.get("birthday") or None
            group_name = row.get("group") or None
            phone = row.get("phone") or None
            phone_type = row.get("phone_type") or "mobile"

            if not username:
                continue

            group_id = None
            if group_name:
                cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
                g = cur.fetchone()
                if g:
                    group_id = g[0]

            cur.execute(
                "INSERT INTO contacts (username,email,birthday,group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                (username, email, birthday, group_id)
            )

            cid = cur.fetchone()[0]

            if phone:
                cur.execute(
                    "INSERT INTO phones (contact_id,phone,type) VALUES (%s,%s,%s)",
                    (cid, phone, phone_type)
                )

    conn.commit()
    cur.close()
    conn.close()


def export_to_json(filename="contacts_export.json"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON g.id=c.group_id
    """)

    data = cur.fetchall()
    result = []

    for cid, username, email, birthday, group_name, created_at in data:
        cur.execute("SELECT phone,type FROM phones WHERE contact_id=%s", (cid,))
        phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]

        result.append({
            "username": username,
            "email": email,
            "birthday": birthday,
            "group": group_name,
            "phones": phones,
            "created_at": str(created_at)
        })

    cur.close()
    conn.close()

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


def import_from_json(filename="contacts_export.json"):
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for r in data:
        username = r["username"]
        email = r["email"]
        birthday = r["birthday"]
        group_name = r["group"]
        phones = r["phones"]

        cur.execute("SELECT id FROM contacts WHERE username=%s", (username,))
        exist = cur.fetchone()

        if exist:
            cid = exist[0]
            cur.execute(
                "UPDATE contacts SET email=%s,birthday=%s WHERE id=%s",
                (email, birthday, cid)
            )
            cur.execute("DELETE FROM phones WHERE contact_id=%s", (cid,))
        else:
            group_id = None
            if group_name:
                cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
                g = cur.fetchone()
                if g:
                    group_id = g[0]

            cur.execute(
                "INSERT INTO contacts (username,email,birthday,group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                (username, email, birthday, group_id)
            )
            cid = cur.fetchone()[0]

        for p in phones:
            cur.execute(
                "INSERT INTO phones (contact_id,phone,type) VALUES (%s,%s,%s)",
                (cid, p["phone"], p.get("type", "mobile"))
            )

    conn.commit()
    cur.close()
    conn.close()


def filter_by_group():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id,name FROM groups")
    groups = cur.fetchall()

    for g in groups:
        print(g)

    gid = input("group id: ")

    cur.execute("""
        SELECT c.id,c.username,c.email,c.birthday,g.name,
        STRING_AGG(p.phone,' | ')
        FROM contacts c
        LEFT JOIN groups g ON g.id=c.group_id
        LEFT JOIN phones p ON p.contact_id=c.id
        WHERE g.id=%s
        GROUP BY c.id,g.name
    """, (gid,))

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()


def search_by_email():
    key = input("email: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id,c.username,c.email
        FROM contacts c
        WHERE c.email ILIKE %s
    """, (f"%{key}%",))

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()


def sorted_list():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id,c.username,c.email
        FROM contacts c
        ORDER BY c.username
    """)

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()


def menu():
    while True:
        print("1 insert")
        print("2 csv")
        print("3 export")
        print("4 import")
        print("5 group")
        print("6 email")
        print("7 sort")
        print("0 exit")

        c = input()

        if c == "1":
            insert_from_console()
        elif c == "2":
            insert_from_csv()
        elif c == "3":
            export_to_json()
        elif c == "4":
            import_from_json()
        elif c == "5":
            filter_by_group()
        elif c == "6":
            search_by_email()
        elif c == "7":
            sorted_list()
        elif c == "0":
            break


if __name__ == "__main__":
    menu()