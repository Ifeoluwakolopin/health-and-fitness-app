import sqlite3


def connect_to_db(db_path):
    return sqlite3.connect(db_path)


def add_user(
    conn, username, age, gender, height, weight, fitness_goals, health_conditions
):
    query = """
    INSERT INTO users (username, age, gender, height, weight, fitness_goals, health_conditions)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (username, age, gender, height, weight, fitness_goals, health_conditions)
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()


def log_workout(
    conn, username, date, time, workout_type, duration, intensity, calories_burned
):
    user_id_query = "SELECT id FROM users WHERE username = ?"
    cur = conn.cursor()
    cur.execute(user_id_query, (username,))
    user_id = cur.fetchone()[0]

    query = """
    INSERT INTO workouts (user_id, date, time, workout_type, duration, intensity, calories_burned)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (user_id, date, time, workout_type, duration, intensity, calories_burned)
    cur.execute(query, params)
    conn.commit()


def record_nutrition(conn, username, date, time, food_item, quantity, calories, macros):
    user_id_query = "SELECT id FROM users WHERE username = ?"
    cur = conn.cursor()
    cur.execute(user_id_query, (username,))
    user_id = cur.fetchone()[0]

    query = """
    INSERT INTO nutrition (user_id, date, time, food_item, quantity, calories, macros)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (user_id, date, time, food_item, quantity, calories, macros)
    cur.execute(query, params)
    conn.commit()


def enter_sleep_data(conn, username, date, sleep_duration, sleep_quality, wake_times):
    user_id_query = "SELECT id FROM users WHERE username = ?"
    cur = conn.cursor()
    cur.execute(user_id_query, (username,))
    user_id = cur.fetchone()[0]

    query = """
    INSERT INTO sleep (user_id, date, sleep_duration, sleep_quality, wake_times)
    VALUES (?, ?, ?, ?, ?);
    """
    params = (user_id, date, sleep_duration, sleep_quality, wake_times)
    cur.execute(query, params)
    conn.commit()


def add_health_metric(
    conn, username, date, time, heart_rate, blood_pressure, blood_sugar, cholesterol
):
    user_id_query = "SELECT id FROM users WHERE username = ?"
    cur = conn.cursor()
    cur.execute(user_id_query, (username,))
    user_id = cur.fetchone()[0]

    query = """
    INSERT INTO health_metrics (user_id, date, time, heart_rate, blood_pressure, blood_sugar, cholesterol)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (user_id, date, time, heart_rate, blood_pressure, blood_sugar, cholesterol)
    cur.execute(query, params)
    conn.commit()


def retrieve_workout_history(conn, username):
    query = """
    SELECT date, workout_type, duration, intensity, calories_burned
    FROM workouts
    WHERE user_id = (SELECT id FROM users WHERE username = ?)
    ORDER BY date DESC;
    """
    cur = conn.cursor()
    cur.execute(query, (username,))
    return cur.fetchall()


def analyze_caloric_intake(conn, username, days_past):
    query = """
    SELECT date, SUM(calories) AS daily_calories
    FROM nutrition
    WHERE user_id = (SELECT id FROM users WHERE username = ?)
    AND date > DATE('now', ?)
    GROUP BY date;
    """
    cur = conn.cursor()
    cur.execute(query, (username, f"-{days_past} days"))
    return cur.fetchall()


def assess_sleep_quality(conn, username, days_past):
    query = """
    SELECT date, AVG(sleep_quality) AS average_quality
    FROM sleep
    WHERE user_id = (SELECT id FROM users WHERE username = ?)
    AND date > DATE('now', ?)
    GROUP BY date;
    """
    cur = conn.cursor()
    cur.execute(query, (username, f"-{days_past} days"))
    return cur.fetchall()


def monitor_health_progress(conn, username):
    query = """
    SELECT date, heart_rate, blood_pressure, blood_sugar, cholesterol
    FROM health_metrics
    WHERE user_id = (SELECT id FROM users WHERE username = ?)
    ORDER BY date ASC;
    """
    cur = conn.cursor()
    cur.execute(query, (username,))
    return cur.fetchall()


# Example usage
if __name__ == "__main__":
    # Connect to the database
    conn = connect_to_db("path_to_your_database.db")

    # Add a new user
    add_user(conn, "JaneDoe", 28, "Female", 165, 60, "Lose weight", "None")

    # Log a workout for 'JaneDoe'
    log_workout(conn, "JaneDoe", "2023-11-09", "08:00", "Cycling", 45, "Moderate", 400)

    # Record a meal for 'JaneDoe'
    record_nutrition(
        conn,
        "JaneDoe",
        "2023-11-09",
        "13:00",
        "Veggie Sandwich",
        2,
        500,
        '{"protein": 20, "carbs": 60, "fat": 10}',
    )

    # Enter sleep data for 'JaneDoe'
    enter_sleep_data(conn, "JaneDoe", "2023-11-08", 420, 7, 1)

    # Add a health metric for 'JaneDoe'
    add_health_metric(conn, "JaneDoe", "2023-11-09", "10:00", 72, "115/75", 85, 190)

    # Retrieve workout history for 'JaneDoe'
    workouts = retrieve_workout_history(conn, "JaneDoe")
    for workout in workouts:
        print(workout)

    # Analyze caloric intake over the past 7 days for 'JaneDoe'
    calories = analyze_caloric_intake(conn, "JaneDoe", 7)
    for cal in calories:
        print(cal)

    # Assess sleep quality over the past month for 'JaneDoe'
    sleep_quality = assess_sleep_quality(conn, "JaneDoe", 30)
    for sleep in sleep_quality:
        print(sleep)

    # Monitor health progress for 'JaneDoe'
    health_progress = monitor_health_progress(conn, "JaneDoe")
    for progress in health_progress:
        print(progress)

    # Close the connection
    conn.close()
