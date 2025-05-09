def insert_health_data(conn, userid, ap_hi, ap_lo, cholesterol, gluc):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v2.health_data (userid, ap_hi, ap_lo, cholesterol, gluc)
            VALUES (%s, %s, %s, %s, %s) RETURNING healthid
        """, (userid, ap_hi, ap_lo, cholesterol, gluc))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted health data ID


def fetch_health_data_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v2.health_data WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns all health data for the given user
