CREATE OR REPLACE PROCEDURE add_phone (
    p_contact_name TEXT,
    p_phone TEXT,
    p_type TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name;

    IF cid IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group (
    p_contact_name TEXT,
    p_group_name TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE gid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group_name;

    IF gid IS NULL THEN
        INSERT INTO groups(name)
        VALUES (p_group_name)
        RETURNING id INTO gid;
    END IF;

    UPDATE contacts
    SET group_id = gid
    WHERE name = p_contact_name;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    name TEXT,
    email TEXT,
    phone TEXT
)
LANGUAGE sql
AS $$
SELECT c.name, c.email, p.phone
FROM contacts c
LEFT JOIN phones p ON c.id = p.contact_id
WHERE
    c.name ILIKE '%'||p_query||'%'
    OR c.email ILIKE '%'||p_query||'%'
    OR p.phone ILIKE '%'||p_query||'%';
$$;