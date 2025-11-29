DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT, -- optional
    status BIT NOT NULL, -- 0 not done, 1 done
    due_date_time DATETIME NOT NULL
);

