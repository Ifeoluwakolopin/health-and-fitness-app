import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create import Base, User, Workout, Nutrition, Sleep, HealthMetric
from insert_data import create_fake_data_orm


class TestDataCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database for testing
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Create fake data in the test database
        create_fake_data_orm(cls.session, num_users=10)

    def test_user_creation(self):
        # Verify that users are created
        user_count = self.session.query(User).count()
        self.assertEqual(user_count, 10)

    def test_workout_creation(self):
        # Verify that workouts are created for each user
        for user in self.session.query(User):
            workouts = self.session.query(Workout).filter_by(user_id=user.id).all()
            self.assertTrue(len(workouts) > 0)

    def test_nutrition_creation(self):
        # Verify that nutrition logs are created for each user
        for user in self.session.query(User):
            nutrition_logs = (
                self.session.query(Nutrition).filter_by(user_id=user.id).all()
            )
            self.assertTrue(len(nutrition_logs) > 0)

    def test_sleep_creation(self):
        # Verify that sleep records are created for each user
        for user in self.session.query(User):
            sleep_records = self.session.query(Sleep).filter_by(user_id=user.id).all()
            self.assertTrue(len(sleep_records) > 0)

    def test_health_metric_creation(self):
        # Verify that health metrics are created for each user
        for user in self.session.query(User):
            health_metrics = (
                self.session.query(HealthMetric).filter_by(user_id=user.id).all()
            )
            self.assertTrue(len(health_metrics) > 0)

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
