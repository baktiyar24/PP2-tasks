import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="snake_game",
        user="postgres",
        password="12345678",
        host="localhost",
        port=5432
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER NOT NULL,
        level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    player = cur.fetchone()

    if player:
        player_id = player[0]
    else:
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return player_id


def save_game(username, score, level):
    player_id = get_or_create_player(username)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    cur.close()
    conn.close()


def get_top_scores():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        WHERE p.username=%s
    """, (username,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result if result else 0