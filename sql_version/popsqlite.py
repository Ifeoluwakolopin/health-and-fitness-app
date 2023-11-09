import sqlite3
import json
from faker import Faker
from tqdm import tqdm
import random
from typing import NoReturn

fake = Faker()


def create_fake_data_sqlite(conn: sqlite3.Connection, num_users: int = 10) -> NoReturn:
    c = conn.cursor()

    # Insert fake users
    for _ in tqdm(range(num_users), desc="Creating Users"):
        c.execute(
            "INSERT INTO users (username, age, gender, height, weight, fitness_goals, health_conditions) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                fake.user_name(),
                random.randint(18, 80),
                random.choice(["Male", "Female", "Non-binary"]),
                round(random.uniform(150.0, 200.0), 2),
                round(random.uniform(50.0, 120.0), 2),
                fake.sentence(),
                random.choice(["None", "Diabetes", "Hypertension", "Asthma"]),
            ),
        )
    conn.commit()

    # Query all users
    c.execute("SELECT id FROM users")
    user_ids = [row[0] for row in c.fetchall()]

    for user_id in tqdm(user_ids, desc="Populating Data for Users"):
        # Workouts
        for _ in range(random.randint(5, 20)):
            c.execute(
                "INSERT INTO workouts (user_id, date, time, workout_type, duration, intensity, calories_burned) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    user_id,
                    fake.date_between(start_date="-1y", end_date="today"),
                    fake.time(),
                    fake.word(
                        ext_word_list=[
                            "Running",
                            "Cycling",
                            "Swimming",
                            "Yoga",
                            "Weightlifting",
                        ]
                    ),
                    random.randint(20, 120),
                    random.choice(["Low", "Medium", "High"]),
                    random.randint(100, 700),
                ),
            )

        # Nutrition logs
        for _ in range(random.randint(10, 30)):
            c.execute(
                "INSERT INTO nutrition (user_id, date, time, food_item, quantity, calories, macros) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    user_id,
                    fake.date_between(start_date="-1y", end_date="today"),
                    fake.time(),
                    fake.word(
                        ext_word_list=[
                            "Salad",
                            "Chicken Breast",
                            "Protein Shake",
                            "Sandwich",
                        ]
                    ),
                    random.randint(1, 3),
                    random.randint(100, 800),
                    json.dumps(
                        {
                            "protein": random.randint(10, 30),
                            "carbs": random.randint(20, 50),
                            "fats": random.randint(5, 20),
                        }
                    ),
                ),
            )

        # Sleep records
        for _ in range(random.randint(50, 100)):
            c.execute(
                "INSERT INTO sleep (user_id, date, sleep_duration, sleep_quality, wake_times) VALUES (?, ?, ?, ?, ?)",
                (
                    user_id,
                    fake.date_between(start_date="-1y", end_date="today"),
                    random.randint(300, 480),
                    random.randint(1, 10),
                    random.randint(0, 5),
                ),
            )

        # Health metrics
        for _ in range(random.randint(10, 30)):
            c.execute(
                "INSERT INTO health_metrics (user_id, date, time, heart_rate, blood_pressure, blood_sugar, cholesterol) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    user_id,
                    fake.date_between(start_date="-1y", end_date="today"),
                    fake.time(),
                    random.randint(60, 100),
                    f"{random.randint(100, 140)}/{random.randint(60, 90)}",
                    random.randint(70, 140),
                    random.randint(100, 200),
                ),
            )

    conn.commit()


# Connect to SQLite database
conn = sqlite3.connect("health_fitness_tracking.db")
create_fake_data_sqlite(conn, 10)
conn.close()
