def insert_insight(conn, userid, healthid, dietaryid, demographicid, predictionid, insight_text):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v1.insight (userid, healthid, dietaryid, demographicid, predictionid, insight_text)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING insightid
        """, (userid, healthid, dietaryid, demographicid, predictionid, insight_text))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted insight ID


def fetch_insights_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v1.insight WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns all insights for a given user
