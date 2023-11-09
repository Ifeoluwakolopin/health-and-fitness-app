from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    Time,
    Text,
    ForeignKey,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, session

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(String(50))
    height = Column(Float)
    weight = Column(Float)
    fitness_goals = Column(Text)
    health_conditions = Column(Text)

    workouts = relationship("Workout", back_populates="user")
    nutrition_logs = relationship("Nutrition", back_populates="user")
    sleep_records = relationship("Sleep", back_populates="user")
    health_metrics = relationship("HealthMetric", back_populates="user")

    # Instance method to add a workout log for the user
    def log_workout(
        self, date, time, workout_type, duration, intensity, calories_burned
    ):
        new_workout = Workout(
            user_id=self.id,
            date=date,
            time=time,
            workout_type=workout_type,
            duration=duration,
            intensity=intensity,
            calories_burned=calories_burned,
        )
        session.add(new_workout)
        session.commit()

    # Instance method to record a nutrition log for the user
    def record_nutrition(self, date, time, food_item, quantity, calories, macros):
        new_nutrition = Nutrition(
            user_id=self.id,
            date=date,
            time=time,
            food_item=food_item,
            quantity=quantity,
            calories=calories,
            macros=macros,
        )
        session.add(new_nutrition)
        session.commit()

    # Instance method to enter sleep data for the user
    def enter_sleep_data(self, date, sleep_duration, sleep_quality, wake_times):
        new_sleep = Sleep(
            user_id=self.id,
            date=date,
            sleep_duration=sleep_duration,
            sleep_quality=sleep_quality,
            wake_times=wake_times,
        )
        session.add(new_sleep)
        session.commit()

    # Instance method to add a health metric for the user
    def add_health_metric(
        self, date, time, heart_rate, blood_pressure, blood_sugar, cholesterol
    ):
        new_health_metric = HealthMetric(
            user_id=self.id,
            date=date,
            time=time,
            heart_rate=heart_rate,
            blood_pressure=blood_pressure,
            blood_sugar=blood_sugar,
            cholesterol=cholesterol,
        )
        session.add(new_health_metric)
        session.commit()


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    time = Column(Time)
    workout_type = Column(String(255))
    duration = Column(Integer)
    intensity = Column(String(50))
    calories_burned = Column(Integer)

    user = relationship("User", back_populates="workouts")


class Nutrition(Base):
    __tablename__ = "nutrition"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    time = Column(Time)
    food_item = Column(String(255))
    quantity = Column(Integer)
    calories = Column(Integer)
    macros = Column(JSON)

    user = relationship("User", back_populates="nutrition_logs")


class Sleep(Base):
    __tablename__ = "sleep"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    sleep_duration = Column(Integer)
    sleep_quality = Column(Integer)
    wake_times = Column(Integer)

    user = relationship("User", back_populates="sleep_records")


class HealthMetric(Base):
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    time = Column(Time)
    heart_rate = Column(Integer)
    blood_pressure = Column(String(50))
    blood_sugar = Column(Integer)
    cholesterol = Column(Integer)

    user = relationship("User", back_populates="health_metrics")


# Create an engine that stores data in the local directory's
# health_fitness_tracking.db file.
engine = create_engine("sqlite:///health_fitness_tracking.db")

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
