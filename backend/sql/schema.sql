CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    info TEXT NOT NULL,
    disclaimer TEXT NOT NULL
);

CREATE TABLE symptom_queries (
    id INTEGER PRIMARY KEY,
    symptoms TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
