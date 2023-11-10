.mode column
.headers on

-- Question: Retrieve the workout history for each user.
SELECT 'Workout history for user: ' || u.username AS question, 
       w.date, 
       w.workout_type, 
       w.duration, 
       w.intensity, 
       w.calories_burned
FROM workouts AS w
JOIN users AS u ON w.user_id = u.id
ORDER BY u.username, w.date DESC;

-- Question: Analyze the caloric intake over the past 7 days for each user.
SELECT 'Caloric intake over the past 7 days for user: ' || u.username AS question, 
       n.date, 
       SUM(n.calories) AS daily_calories
FROM nutrition AS n
JOIN users AS u ON n.user_id = u.id
WHERE n.date > DATE('now', '-7 days')
GROUP BY u.username, n.date
ORDER BY u.username, n.date DESC;

-- Question: Assess the sleep quality over the past 30 days for each user.
SELECT 'Sleep quality over the past 30 days for user: ' || u.username AS question, 
       s.date, 
       AVG(s.sleep_quality) AS average_quality
FROM sleep AS s
JOIN users AS u ON s.user_id = u.id
WHERE s.date > DATE('now', '-30 days')
GROUP BY u.username, s.date
ORDER BY u.username, s.date DESC;

-- Question: Monitor the health progress for each user by retrieving the latest health metric record.
SELECT 'Latest health metric record for user: ' || u.username AS question, 
       hm.date, 
       hm.heart_rate, 
       hm.blood_pressure, 
       hm.blood_sugar, 
       hm.cholesterol
FROM health_metrics AS hm
JOIN users AS u ON hm.user_id = u.id
WHERE hm.date = (SELECT MAX(hm2.date) FROM health_metrics AS hm2 WHERE hm2.user_id = hm.user_id)
ORDER BY u.username, hm.date DESC;

-- Additional questions might include:

-- Question: Who has burned the most calories in a single workout session?
SELECT 'User who burned the most calories in a single workout session: ' AS question,
       u.username, 
       MAX(w.calories_burned) AS max_calories
FROM workouts AS w
JOIN users AS u ON w.user_id = u.id
GROUP BY u.username
ORDER BY max_calories DESC
LIMIT 1;

-- Question: What is the average sleep duration for each user in the past week?
SELECT 'Average sleep duration for the past week for user: ' || u.username AS question,
       AVG(s.sleep_duration) AS average_sleep_duration
FROM sleep AS s
JOIN users AS u ON s.user_id = u.id
WHERE s.date > DATE('now', '-7 days')
GROUP BY u.username
ORDER BY average_sleep_duration DESC;

-- Question: Which user has the highest average heart rate in their health metrics?
SELECT 'User with the highest average heart rate in health metrics: ' AS question,
       u.username, 
       AVG(hm.heart_rate) AS average_heart_rate
FROM health_metrics AS hm
JOIN users AS u ON hm.user_id = u.id
GROUP BY u.username
ORDER BY average_heart_rate DESC
LIMIT 1;

-- Question: Find the user with the highest average workout duration.
SELECT 'User with the highest average workout duration: ' AS question,
       u.username, 
       AVG(w.duration) AS avg_duration
FROM workouts AS w
JOIN users AS u ON w.user_id = u.id
GROUP BY u.username
ORDER BY avg_duration DESC
LIMIT 1;

-- Question: Identify the most popular workout type among all users.
SELECT 'Most popular workout type: ' AS question,
       workout_type, 
       COUNT(*) AS count
FROM workouts
GROUP BY workout_type
ORDER BY count DESC
LIMIT 1;

-- Question: Calculate the average caloric intake per meal for each user.
SELECT 'Average caloric intake per meal for user: ' || u.username AS question,
       AVG(n.calories / n.quantity) AS avg_calories_per_meal
FROM nutrition AS n
JOIN users AS u ON n.user_id = u.id
GROUP BY u.username
ORDER BY avg_calories_per_meal DESC;

-- Question: Identify the day of the week with the most workouts.
SELECT 'Day of the week with the most workouts: ' AS question,
       strftime('%w', date) AS day_of_week, 
       COUNT(*) AS workout_count
FROM workouts
GROUP BY day_of_week
ORDER BY workout_count DESC
LIMIT 1;

-- Question: Determine the user with the most consistent sleep schedule (least variation in sleep duration).
SELECT 'User with the most consistent sleep schedule: ' AS question,
       u.username, 
       MIN(ABS(AVG(s.sleep_duration) - s.sleep_duration)) AS min_variation
FROM sleep AS s
JOIN users AS u ON s.user_id = u.id
GROUP BY u.username
ORDER BY min_variation ASC
LIMIT 1;

-- Question: List the personal best for calories burned in a single workout session by each user.
SELECT 'Personal best for calories burned in a workout by user: ' || u.username AS question,
       MAX(w.calories_burned) AS personal_best_calories
FROM workouts AS w
JOIN users AS u ON w.user_id = u.id
GROUP BY u.username
ORDER BY personal_best_calories DESC;

-- Question: Show the trend of workout intensity for each user over time.
SELECT 'Workout intensity trend for user: ' || u.username AS question,
       w.date, 
       w.intensity
FROM workouts AS w
JOIN users AS u ON w.user_id = u.id
ORDER BY u.username, w.date;

-- Question: Retrieve users' latest blood pressure readings.
SELECT 'Latest blood pressure reading for user: ' || u.username AS question,
       hm.blood_pressure
FROM health_metrics AS hm
JOIN users AS u ON hm.user_id = u.id
WHERE hm.date = (SELECT MAX(date) FROM health_metrics WHERE user_id = hm.user_id)
ORDER BY u.username;