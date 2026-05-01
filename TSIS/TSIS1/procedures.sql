CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE username = p_contact_name;

    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type "%". Use home, work, or mobile.', p_type;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;


DROP FUNCTION IF EXISTS search_contacts(TEXT);

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    username   VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phone      VARCHAR,
    phone_type VARCHAR,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT ON (c.id, ph.phone)
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name,
        ph.phone,
        ph.type,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE
        c.username ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR ph.phone ILIKE '%' || p_query || '%'
    ORDER BY c.id, ph.phone;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);

CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE (
    id         INTEGER,
    username   VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones_agg TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name,
        STRING_AGG(ph.phone || ' (' || ph.type || ')', ', '),
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    GROUP BY c.id, c.username, c.email, c.birthday, g.name, c.created_at
    ORDER BY c.username
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;