import json
import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from create import Base, User, Workout, Nutrition, Sleep, HealthMetric

# Configure a test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"


class TestUserModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database for testing
        cls.engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.session_factory = sessionmaker(bind=cls.engine)
        cls.session = scoped_session(cls.session_factory)

    @classmethod
    def tearDownClass(cls):
        # Drop the test database
        Base.metadata.drop_all(cls.engine)
        cls.session.remove()

    def setUp(self):
        # Start a new transaction for each test
        self.session = self.session_factory()

    def tearDown(self):
        # Rollback the session after each test
        self.session.rollback()
        self.session.close()

    def test_user_creation(self):
        # Test user creation
        user = User(username="testuser", age=30, gender="Other", height=170, weight=70)
        self.session.add(user)
        self.session.commit()
        self.assertIsNotNone(user.id, "User ID should be set after saving.")

    def test_log_workout(self):
        # Retrieve user from the database or create a new one for testing
        user = self.session.query(User).filter_by(username="testuser").first()
        if not user:
            user = User(
                username="testuser", age=30, gender="Other", height=170, weight=70
            )
            self.session.add(user)
            self.session.commit()

        # Convert string date and time to datetime objects
        date_obj = datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        time_obj = datetime.strptime("12:00:00", "%H:%M:%S").time()

        # Use the instance method to log a workout
        user.log_workout(
            self.session,
            date=date_obj,
            time=time_obj,
            workout_type="Running",
            duration=60,
            intensity="Medium",
            calories_burned=500,
        )
        self.session.commit()

        # Query the database to ensure the workout was logged correctly
        workout = self.session.query(Workout).filter_by(user_id=user.id).first()
        self.assertIsNotNone(workout)
        self.assertEqual(workout.intensity, "Medium")

    def test_record_nutrition(self):
        # Test recording a nutrition log
        user = User(
            username="nutritionuser", age=30, gender="Other", height=170, weight=70
        )
        self.session.add(user)
        self.session.commit()

        # Convert string date and time to date and time objects
        date_obj = datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        time_obj = datetime.strptime("12:00:00", "%H:%M:%S").time()

        macros = {"protein": 20, "carbs": 50, "fats": 10}
        user.record_nutrition(
            self.session,
            date=date_obj,
            time=time_obj,
            food_item="Salad",
            quantity=1,
            calories=300,
            macros=json.dumps(macros),
        )
        self.session.commit()

        nutrition = self.session.query(Nutrition).filter_by(user_id=user.id).first()
        self.assertIsNotNone(nutrition, "Nutrition record should be created.")
        self.assertEqual(nutrition.calories, 300, "Calories should be 300.")

    def test_enter_sleep_data(self):
        # Test entering sleep data
        user = User(username="sleepuser", age=30, gender="Other", height=170, weight=70)
        self.session.add(user)
        self.session.commit()

        # Convert string date and time to date and time objects
        date_obj = datetime.strptime("2022-01-01", "%Y-%m-%d").date()

        user.enter_sleep_data(
            self.session,
            date=date_obj,
            sleep_duration=480,
            sleep_quality=4,
            wake_times=2,
        )
        self.session.commit()

        sleep = self.session.query(Sleep).filter_by(user_id=user.id).first()
        self.assertIsNotNone(sleep, "Sleep record should be created.")
        self.assertEqual(sleep.sleep_quality, 4, "Sleep quality should be 4.")

    def test_add_health_metric(self):
        # Test adding a health metric
        user = User(
            username="healthmetricuser", age=30, gender="Other", height=170, weight=70
        )
        self.session.add(user)
        self.session.commit()

        # Convert string date and time to date and time objects
        date_obj = datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        time_obj = datetime.strptime("12:00:00", "%H:%M:%S").time()

        user.add_health_metric(
            self.session,
            date=date_obj,
            time=time_obj,
            heart_rate=80,
            blood_pressure="120/80",
            blood_sugar=90,
            cholesterol=200,
        )
        self.session.commit()

        health_metric = (
            self.session.query(HealthMetric).filter_by(user_id=user.id).first()
        )
        self.assertIsNotNone(health_metric, "Health metric should be created.")
        self.assertEqual(health_metric.heart_rate, 80, "Heart rate should be 80.")
