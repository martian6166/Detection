def insert_demographic_data(conn, userid, age, education_level, incomestatus, gender):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v1.demographicdata (userid, age, educationlevel, incomestatus, gender)
            VALUES (%s, %s, %s, %s, %s) RETURNING demographicid
        """, (userid, age, education_level, incomestatus, gender))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted demographic ID

def fetch_demographic_data_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v1.demographicdata WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns demographic data for a given user
