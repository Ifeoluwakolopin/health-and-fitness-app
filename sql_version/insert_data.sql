BEGIN TRANSACTION;

-- Inserting sample users
INSERT INTO users (username, age, gender, height, weight, fitness_goals, health_conditions) VALUES 
('johndoe_1', 28, 'Male', 180, 82, 'Weight loss', 'None'),
('janedoe_2', 34, 'Female', 162, 64, 'Cardio training', 'Asthma'),
('mikebrown_3', 41, 'Male', 175, 90, 'Muscle gain', 'None'),
('lucywhite_4', 29, 'Female', 170, 70, 'Flexibility and toning', 'None'),
('tomblack_5', 36, 'Male', 182, 85, 'Endurance', 'Diabetes');

-- Inserting workouts, each user will have two entries
-- Each user_id from 1 to 5 will be associated with the workouts
INSERT INTO workouts (user_id, date, time, workout_type, duration, intensity, calories_burned) VALUES 
(1, '2023-01-01', '07:00', 'Running', 30, 'High', 300),
(1, '2023-01-02', '06:00', 'Swimming', 60, 'Medium', 250),
(2, '2023-01-03', '18:00', 'Cycling', 45, 'Low', 200),
(2, '2023-01-04', '20:00', 'Yoga', 40, 'Low', 100),
(3, '2023-01-05', '05:30', 'Gym', 60, 'High', 500),
(3, '2023-01-06', '19:00', 'Boxing', 45, 'High', 450),
(4, '2023-01-07', '08:00', 'Pilates', 50, 'Medium', 180),
(4, '2023-01-08', '17:00', 'Dance', 60, 'High', 300),
(5, '2023-01-09', '06:30', 'Rowing', 70, 'Medium', 400),
(5, '2023-01-10', '18:30', 'HIIT', 30, 'High', 350);

-- Inserting nutrition logs, each user will have two entries
-- Each user_id from 1 to 5 will be associated with the nutrition logs
INSERT INTO nutrition (user_id, date, time, food_item, quantity, calories, macros) VALUES 
(1, '2023-01-01', '08:00', 'Oatmeal', 2, 300, '{"protein": 10, "carbs": 50, "fats": 6}'),
(1, '2023-01-02', '13:00', 'Chicken Salad', 1, 350, '{"protein": 30, "carbs": 10, "fats": 20}'),
(2, '2023-01-03', '09:00', 'Protein Shake', 1, 250, '{"protein": 25, "carbs": 5, "fats": 2}'),
(2, '2023-01-04', '19:00', 'Steak and Veggies', 1, 500, '{"protein": 40, "carbs": 20, "fats": 30}'),
(3, '2023-01-05', '07:30', 'Eggs and Toast', 2, 350, '{"protein": 20, "carbs": 30, "fats": 12}'),
(3, '2023-01-06', '12:30', 'Tuna Sandwich', 1, 400, '{"protein": 35, "carbs": 40, "fats": 10}'),
(4, '2023-01-07', '08:15', 'Fruit Salad', 3, 330, '{"protein": 5, "carbs": 80, "fats": 3}'),
(4, '2023-01-08', '18:45', 'Vegetable Stir Fry', 1, 375, '{"protein": 12, "carbs": 60, "fats": 9}'),
(5, '2023-01-09', '07:45', 'Greek Yogurt', 2, 280, '{"protein": 24, "carbs": 40, "fats": 4}'),
(5, '2023-01-10', '13:15', 'Quinoa Salad', 1, 410, '{"protein": 15, "carbs": 70, "fats": 10}');

-- Inserting sleep records, each user will have two entries
-- Each user_id from 1 to 5 will be associated with the sleep records
INSERT INTO sleep (user_id, date, sleep_duration, sleep_quality, wake_times) VALUES 
(1, '2023-01-01', 420, 8, 0),
(1, '2023-01-02', 390, 7, 1),
(2, '2023-01-03', 480, 9, 0),
(2, '2023-01-04', 460, 8, 1),
(3, '2023-01-05', 430, 7, 2),
(3, '2023-01-06', 400, 6, 1),
(4, '2023-01-07', 450, 8, 0),
(4, '2023-01-08', 370, 7, 3),
(5, '2023-01-09', 440, 8, 1),
(5, '2023-01-10', 410, 7, 2);

-- Inserting health metrics, each user will have two entries
-- Each user_id from 1 to 5 will be associated with the health metrics
INSERT INTO health_metrics (user_id, date, time, heart_rate, blood_pressure, blood_sugar, cholesterol) VALUES 
(1, '2023-01-01', '07:00', 65, '125/80', 95, 180),
(1, '2023-01-02', '20:00', 70, '126/79', 90, 175),
(2, '2023-01-03', '06:30', 68, '120/75', 88, 170),
(2, '2023-01-04', '21:00', 72, '122/76', 85, 165),
(3, '2023-01-05', '07:15', 75, '127/78', 92, 185),
(3, '2023-01-06', '19:30', 73, '123/77', 87, 175),
(4, '2023-01-07', '06:45', 60, '119/74', 93, 190),
(4, '2023-01-08', '20:15', 71, '121/75', 89, 180),
(5, '2023-01-09', '07:30', 69, '124/78', 91, 185),
(5, '2023-01-10', '19:45', 74, '128/80', 86, 170);

COMMIT;
