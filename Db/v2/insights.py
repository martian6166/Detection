def insert_insight(conn, userid, healthid, predictionid, insight_text):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v2.insights (userid, healthid, predictionid, insight_text)
            VALUES (%s, %s, %s, %s) RETURNING insightid
        """, (userid, healthid, predictionid, insight_text))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted insight ID


def fetch_insights_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v2.insights WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns all insights for the given user
