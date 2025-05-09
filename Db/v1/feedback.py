def insert_feedback(conn, userid, healthid, dietaryid, demographicid, user_feedback):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v1.feedback (userid, healthid, dietaryid, demographicid, userfeedback)
            VALUES (%s, %s, %s, %s, %s) RETURNING feedbackid
        """, (userid, healthid, dietaryid, demographicid, user_feedback))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted feedback ID

def fetch_feedback_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v1.feedback WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns all feedback for a given user
