def insert_feedback(conn, userid, healthid, predictionid, userfeedback):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v2.feedback (userid, healthid, predictionid, userfeedback)
            VALUES (%s, %s, %s, %s) RETURNING feedbackid
        """, (userid, healthid, predictionid, userfeedback))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted feedback ID

def fetch_feedback_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v2.feedback WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns all feedback for the given user
