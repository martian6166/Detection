def insert_prediction(conn, userid, healthid, cardio):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v2.predictions (userid, healthid, cardio)
            VALUES (%s, %s, %s) RETURNING predictionid
        """, (userid, healthid, cardio))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted prediction ID

def fetch_predictions_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v2.predictions WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns all predictions for the given user
