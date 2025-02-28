import psycopg2

def insert_user(conn, age, gender, height, weight, smoke, alco, active):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v2.users (age, gender, height, weight, smoke, alco, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING userid
        """, (age, gender, height, weight, smoke, alco, active))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted user's ID


def fetch_users(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v2.users")
        return cursor.fetchall()  # Returns a list of all users
