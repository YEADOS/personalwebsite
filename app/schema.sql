DROP TABLE IF EXISTS user; 
DROP TABLE IF EXISTS streak;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE streak (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    streak_start_date DATE DEFAULT NULL,
    streak_last_date DATE DEFAULT NULL
);

-- Ensure initial streak record exists
INSERT INTO streak (id, current_streak, longest_streak, streak_start_date, streak_last_date) 
VALUES (1, 0, 0, NULL, "2025-03-19");