# Want to let bot pull from database
import sqlite3

conn = sqlite3.connect ('trivia.db')
c = conn.cursor()

c = conn.cursor()

c.execute('DROP TABLE trivia')

c.execute('''CREATE TABLE trivia
             (q_id INTEGER PRIMARY KEY NOT NULL, question text, answer text, category text, value integer)''')

c.execute('INSERT INTO trivia(question, answer, category, value) VALUES ("What is your name 1?", "answer1", "General", 200)')
c.execute('INSERT INTO trivia(question, answer, category, value) VALUES ("What is your name 2?", "answer2", "General", 300)')
c.execute('INSERT INTO trivia(question, answer, category, value) VALUES ("What is your name 3?", "answer3", "General", 400)')

conn.commit()


conn.close()
