from models import User, Workout, Nutrition, Sleep, HealthMetric, session, engine
from faker import Faker
import random
from datetime import timedelta, datetime

fake = Faker()


def create_fake_data_orm(num_users=10):
    users = []
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            age=random.randint(18, 80),
            gender=random.choice(["Male", "Female", "Non-binary"]),
            height=round(random.uniform(150.0, 200.0), 2),
            weight=round(random.uniform(50.0, 120.0), 2),
            fitness_goals=fake.sentence(),
            health_conditions=fake.word(
                ext_word_list=["None", "Diabetes", "Hypertension", "Asthma"]
            ),
        )
        users.append(user)

    session.add_all(users)
    session.commit()

    for user in users:
        # Create random workouts
        for _ in range(random.randint(5, 20)):  # Random number of workouts
            date = fake.date_between(start_date="-1y", end_date="today")
            workout = Workout(
                user_id=user.id,
                date=date,
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
                duration=random.randint(20, 120),  # Duration in minutes
                intensity=random.choice(["Low", "Medium", "High"]),
                calories_burned=random.randint(100, 700),
            )
            session.add(workout)

        # Create random nutrition logs
        for _ in range(random.randint(10, 30)):  # Random number of meals
            nutrition = Nutrition(
                user_id=user.id,
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
            session.add(nutrition)

        # Create random sleep records
        for _ in range(random.randint(50, 100)):  # Random number of sleep records
            sleep = Sleep(
                user_id=user.id,
                date=fake.date_between(start_date="-1y", end_date="today"),
                sleep_duration=random.randint(300, 480),  # Duration in minutes
                sleep_quality=random.randint(1, 10),
                wake_times=random.randint(0, 5),
            )
            session.add(sleep)

        # Create random health metrics
        for _ in range(random.randint(10, 30)):  # Random number of health metrics
            health_metric = HealthMetric(
                user_id=user.id,
                date=fake.date_between(start_date="-1y", end_date="today"),
                time=fake.time(),
                heart_rate=random.randint(60, 100),
                blood_pressure=f"{random.randint(100, 140)}/{random.randint(60, 90)}",
                blood_sugar=random.randint(70, 140),
                cholesterol=random.randint(100, 200),
            )
            session.add(health_metric)

    session.commit()


create_fake_data_orm(10)
