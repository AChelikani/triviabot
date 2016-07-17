import sqlite3

conn = sqlite3.connect ('trivia.db')
c = conn.cursor()

c = conn.cursor()

c.execute('DROP TABLE trivia')

c.execute('''CREATE TABLE trivia
             (q_id INTEGER PRIMARY KEY NOT NULL, question text, answer text, category text, value integer)''')

c.execute('INSERT INTO trivia(question, answer, category, value) VALUES ("What is your name 1?", "Saanvi", "General", 200)')
c.execute('INSERT INTO trivia(question, answer, category, value) VALUES ("What is your name 2?", "Saanvi", "General", 200)')
c.execute('INSERT INTO trivia(question, answer, category, value) VALUES ("What is your name 3?", "Saanvi", "General", 200)')

conn.commit()


conn.close()
