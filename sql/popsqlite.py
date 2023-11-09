import sqlite3
import json
from faker import Faker
import random
from datetime import timedelta, datetime

fake = Faker()

conn = sqlite3.connect("health_fitness_tracking.db")
c = conn.cursor()


def create_fake_data_sqlite(num_users=10):
    # Insert fake users
    for _ in range(num_users):
        c.execute(
            "INSERT INTO users (username, age, gender, height, weight, fitness_goals, health_conditions) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                fake.user_name(),
                random.randint(18, 80),
                random.choice(["Male", "Female", "Non-binary"]),
                round(random.uniform(150.0, 200.0), 2),
                round(random.uniform(50.0, 120.0), 2),
                fake.sentence(),
                fake.word(ext_word_list=["None", "Diabetes", "Hypertension", "Asthma"]),
            ),
        )
    conn.commit()

    # Query all users
    c.execute("SELECT id FROM users")
    user_ids = [row[0] for row in c.fetchall()]

    for user_id in user_ids:
        # Insert fake workouts
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

        # Insert fake nutrition logs
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

        # Insert fake sleep records
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

        # Insert fake health metrics
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


create_fake_data_sqlite(10)
conn.close()
