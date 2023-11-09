-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    fitness_goals TEXT,
    health_conditions TEXT
);

-- Workouts Table
CREATE TABLE workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    time TIME,
    workout_type TEXT,
    duration INTEGER,
    intensity TEXT,
    calories_burned INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Nutrition Table
CREATE TABLE nutrition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    time TIME,
    food_item TEXT,
    quantity INTEGER,
    calories INTEGER,
    macros TEXT, -- stored as a JSON string
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Sleep Table
CREATE TABLE sleep (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    sleep_duration INTEGER,
    sleep_quality INTEGER,
    wake_times INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Health Metrics Table
CREATE TABLE health_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    time TIME,
    heart_rate INTEGER,
    blood_pressure TEXT,
    blood_sugar INTEGER,
    cholesterol INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Indexes

-- Create an index on the username column in the users table
CREATE INDEX idx_username ON users(username);

-- Create an index on the user_id column in the workouts table
CREATE INDEX idx_workouts_user_id ON workouts(user_id);

-- Repeat for other tables and foreign key columns as necessary
CREATE INDEX idx_nutrition_user_id ON nutrition(user_id);
CREATE INDEX idx_sleep_user_id ON sleep(user_id);
CREATE INDEX idx_health_metrics_user_id ON health_metrics(user_id);
