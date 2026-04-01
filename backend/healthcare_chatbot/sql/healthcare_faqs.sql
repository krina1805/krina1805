CREATE TABLE IF NOT EXISTS healthcare_faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

INSERT INTO healthcare_faqs (question, answer) VALUES
('What are common symptoms of flu?', 'Common flu symptoms include fever, cough, sore throat, body aches, fatigue, and chills.'),
('How much water should I drink daily?', 'Many adults benefit from roughly 2 to 3 liters of fluids daily, but needs vary by person and climate.'),
('How can I improve sleep quality?', 'Keep a regular sleep schedule, reduce evening caffeine, avoid heavy meals late, and create a dark, quiet bedroom.');
