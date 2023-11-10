from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from create import User, Workout, Nutrition, Sleep, HealthMetric
from datetime import datetime, timedelta
from tabulate import tabulate

# Set up the engine and session
engine = create_engine("sqlite:///health_fitness_tracking.db")
Session = sessionmaker(bind=engine)
session = Session()


def print_table(question, data, headers):
    print(question)
    print(tabulate(data, headers=headers, tablefmt="pretty"))


def workout_history(username: str):
    """Retrieve the workout history for a given user."""
    user = session.query(User).filter(User.username == username).first()
    if user:
        workouts = (
            session.query(
                Workout.date,
                Workout.workout_type,
                Workout.duration,
                Workout.calories_burned,
            )
            .filter(Workout.user_id == user.id)
            .order_by(Workout.date.desc())
            .all()
        )

        print_table(
            "Workout History:",
            workouts,
            ["Date", "Type", "Duration (min)", "Calories Burned"],
        )


def caloric_intake_analysis(username: str, days_past: int):
    """Analyze the caloric intake for a given user over a specified number of past days."""
    user = session.query(User).filter(User.username == username).first()
    if user:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_past)
        nutrition_data = (
            session.query(
                Nutrition.date, func.sum(Nutrition.calories).label("daily_calories")
            )
            .filter(
                Nutrition.user_id == user.id,
                Nutrition.date.between(start_date, end_date),
            )
            .group_by(Nutrition.date)
            .all()
        )

        print_table(
            "Caloric Intake Analysis:", nutrition_data, ["Date", "Daily Calories"]
        )


def sleep_quality_assessment(username: str, days_past: int):
    """Assess the sleep quality over a specified number of past days for a given user."""
    user = session.query(User).filter(User.username == username).first()
    if user:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_past)
        sleep_data = (
            session.query(
                Sleep.date, func.avg(Sleep.sleep_quality).label("average_quality")
            )
            .filter(Sleep.user_id == user.id, Sleep.date.between(start_date, end_date))
            .group_by(Sleep.date)
            .all()
        )

        print_table(
            "Sleep Quality Assessment:", sleep_data, ["Date", "Average Sleep Quality"]
        )


def health_progress_monitoring(username: str):
    """Monitor the health progress for a given user by retrieving their health metric history."""
    user = session.query(User).filter(User.username == username).first()
    if user:
        health_metrics = (
            session.query(
                HealthMetric.date,
                HealthMetric.heart_rate,
                HealthMetric.blood_pressure,
                HealthMetric.blood_sugar,
                HealthMetric.cholesterol,
            )
            .filter(HealthMetric.user_id == user.id)
            .order_by(HealthMetric.date.asc())
            .all()
        )

        print_table(
            "Health Progress Monitoring:",
            health_metrics,
            ["Date", "Heart Rate", "Blood Pressure", "Blood Sugar", "Cholesterol"],
        )


if __name__ == "__main__":
    # Fetch all usernames from the database
    usernames = session.query(User.username).all()
    usernames = [username[0] for username in usernames]  # Unpack tuples

    # Perform queries for each user
    for username in usernames:
        print(f"\n==== User: {username} ====")
        workout_history(username)
        caloric_intake_analysis(username, 7)
        sleep_quality_assessment(username, 30)
        health_progress_monitoring(username)

    session.close()
