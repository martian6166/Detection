
def insert_health_data(conn, userid, highly_bp, high_cholesterol, num_bp_adverse, bmi, stroke_event):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v1.healthdata (userid, highly, highcholesterol, numberofcholesteroladverse, bmi, eventofbpandstroke)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING healthid
        """, (userid, highly_bp, high_cholesterol, num_bp_adverse, bmi, stroke_event))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted health ID


def fetch_health_data_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v1.healthdata WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns health data for a given user
