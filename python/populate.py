from models import User, Workout, Nutrition, Sleep, HealthMetric, session, engine
from faker import Faker
from tqdm import tqdm
import random
import json
from typing import NoReturn

fake = Faker()


def create_fake_data_orm(num_users: int = 10) -> NoReturn:
    users = []
    for _ in tqdm(range(num_users), desc="Creating Users"):
        user = User(
            username=fake.user_name(),
            age=random.randint(18, 80),
            gender=random.choice(["Male", "Female", "Non-binary"]),
            height=round(random.uniform(150.0, 200.0), 2),
            weight=round(random.uniform(50.0, 120.0), 2),
            fitness_goals=fake.sentence(),
            health_conditions=random.choice(
                ["None", "Diabetes", "Hypertension", "Asthma"]
            ),
        )
        users.append(user)

    session.add_all(users)
    session.commit()

    for user in tqdm(users, desc="Populating Data for Users"):
        # Workouts
        for _ in range(random.randint(5, 20)):
            user.log_workout(
                date=fake.date_between(start_date="-1y", end_date="today"),
                time=fake.time(),
                workout_type=fake.word(
                    ext_word_list=[
                        "Running",
                        "Cycling",
                        "Swimming",
                        "Yoga",
                        "Weightlifting",
                    ]
                ),
                duration=random.randint(20, 120),
                intensity=random.choice(["Low", "Medium", "High"]),
                calories_burned=random.randint(100, 700),
            )

        # Nutrition logs
        for _ in range(random.randint(10, 30)):
            user.record_nutrition(
                date=fake.date_between(start_date="-1y", end_date="today"),
                time=fake.time(),
                food_item=fake.word(
                    ext_word_list=[
                        "Salad",
                        "Chicken Breast",
                        "Protein Shake",
                        "Sandwich",
                    ]
                ),
                quantity=random.randint(1, 3),
                calories=random.randint(100, 800),
                macros=json.dumps(
                    {
                        "protein": random.randint(10, 30),
                        "carbs": random.randint(20, 50),
                        "fats": random.randint(5, 20),
                    }
                ),
            )

        # Sleep records
        for _ in range(random.randint(50, 100)):
            user.enter_sleep_data(
                date=fake.date_between(start_date="-1y", end_date="today"),
                sleep_duration=random.randint(300, 480),
                sleep_quality=random.randint(1, 10),
                wake_times=random.randint(0, 5),
            )

        # Health metrics
        for _ in range(random.randint(10, 30)):
            user.add_health_metric(
                date=fake.date_between(start_date="-1y", end_date="today"),
                time=fake.time(),
                heart_rate=random.randint(60, 100),
                blood_pressure=f"{random.randint(100, 140)}/{random.randint(60, 90)}",
                blood_sugar=random.randint(70, 140),
                cholesterol=random.randint(100, 200),
            )


create_fake_data_orm(10)
