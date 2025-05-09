def insert_dietary_data(conn, userid, consumed_fruits):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v1.dietarydata (userid, consumedfruitswithin30days)
            VALUES (%s, %s) RETURNING dietaryid
        """, (userid, consumed_fruits))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted dietary ID


def fetch_dietary_data_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v1.dietarydata WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns dietary data for a given user
