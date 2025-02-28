def insert_prediction(conn, userid, healthid, dietaryid, demographicid, prediction_results):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO v1.prediction (userid, healthid, dietaryid, demographicid, predictionresults)
            VALUES (%s, %s, %s, %s, %s) RETURNING predictionid
        """, (userid, healthid, dietaryid, demographicid, prediction_results))
        conn.commit()
        return cursor.fetchone()[0]  # Returns the inserted prediction ID


def fetch_predictions_by_user(conn, userid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM v1.prediction WHERE userid = %s", (userid,))
        return cursor.fetchall()  # Returns all predictions for a given user
