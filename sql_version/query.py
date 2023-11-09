import sqlite3
from typing import List, Tuple, NoReturn


def connect_to_db(db_path: str) -> sqlite3.Connection:
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(db_path)


def add_user(
    conn: sqlite3.Connection,
    username: str,
    age: int,
    gender: str,
    height: float,
    weight: float,
    fitness_goals: str,
    health_conditions: str,
) -> NoReturn:
    """
    Add a new user to the database.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.
    - age: The age of the user.
    - gender: The gender of the user.
    - height: The height of the user.
    - weight: The weight of the user.
    - fitness_goals: The fitness goals of the user.
    - health_conditions: The health conditions of the user.
    """
    query = """
    INSERT INTO users (username, age, gender, height, weight, fitness_goals, health_conditions)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (username, age, gender, height, weight, fitness_goals, health_conditions)
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()


def log_workout(
    conn: sqlite3.Connection,
    username: str,
    date: str,
    time: str,
    workout_type: str,
    duration: int,
    intensity: str,
    calories_burned: int,
) -> NoReturn:
    """
    Log a workout session for a user in the database.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.
    - date: The date of the workout.
    - time: The time when the workout started.
    - workout_type: The type of workout.
    - duration: The duration of the workout in minutes.
    - intensity: The intensity of the workout.
    - calories_burned: The number of calories burned during the workout.
    """
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


def record_nutrition(
    conn: sqlite3.Connection,
    username: str,
    date: str,
    time: str,
    food_item: str,
    quantity: int,
    calories: int,
    macros: str,
) -> NoReturn:
    """
    Record a nutrition log for a user in the database.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.
    - date: The date of the meal.
    - time: The time when the meal was consumed.
    - food_item: The food item consumed.
    - quantity: The quantity of the food item.
    - calories: The total calories of the meal.
    - macros: The macronutrient breakdown of the meal.
    """
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


def enter_sleep_data(
    conn: sqlite3.Connection,
    username: str,
    date: str,
    sleep_duration: int,
    sleep_quality: int,
    wake_times: int,
) -> NoReturn:
    """
    Enter sleep data for a user in the database.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.
    - date: The date of the sleep record.
    - sleep_duration: The total duration of sleep in minutes.
    - sleep_quality: The quality of sleep on a scale of 1 to 10.
    - wake_times: The number of times the user woke up during sleep.
    """
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
    conn: sqlite3.Connection,
    username: str,
    date: str,
    time: str,
    heart_rate: int,
    blood_pressure: str,
    blood_sugar: int,
    cholesterol: int,
) -> NoReturn:
    """
    Add a health metric record for a user in the database.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.
    - date: The date of the health metric record.
    - time: The time when the health metric was recorded.
    - heart_rate: The heart rate of the user.
    - blood_pressure: The blood pressure of the user.
    - blood_sugar: The blood sugar level of the user.
    - cholesterol: The cholesterol level of the user.
    """
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


def retrieve_workout_history(conn: sqlite3.Connection, username: str) -> List[Tuple]:
    """
    Retrieve the workout history of a user from the database.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.

    Returns:
    - A list of tuples containing the workout history data.
    """
    query = """
    SELECT date, workout_type, duration, intensity, calories_burned
    FROM workouts
    WHERE user_id = (SELECT id FROM users WHERE username = ?)
    ORDER BY date DESC;
    """
    cur = conn.cursor()
    cur.execute(query, (username,))
    return cur.fetchall()


def analyze_caloric_intake(
    conn: sqlite3.Connection, username: str, days_past: int
) -> List[Tuple]:
    """
    Analyze the caloric intake of a user over a specified number of past days.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.
    - days_past: The number of past days to analyze.

    Returns:
    - A list of tuples containing the caloric intake data.
    """
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


def assess_sleep_quality(
    conn: sqlite3.Connection, username: str, days_past: int
) -> List[Tuple]:
    """
    Assess the sleep quality of a user over a specified number of past days.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.
    - days_past: The number of past days to assess.

    Returns:
    - A list of tuples containing the sleep quality data.
    """
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


def monitor_health_progress(conn: sqlite3.Connection, username: str) -> List[Tuple]:
    """
    Monitor the health progress of a user by retrieving their health metric history.

    Parameters:
    - conn: The database connection object.
    - username: The username of the user.

    Returns:
    - A list of tuples containing the health metric data.
    """
    query = """
    SELECT date, heart_rate, blood_pressure, blood_sugar, cholesterol
    FROM health_metrics
    WHERE user_id = (SELECT id FROM users WHERE username = ?)
    ORDER BY date ASC;
    """
    cur = conn.cursor()
    cur.execute(query, (username,))
    return cur.fetchall()
