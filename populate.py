# Want to let bot pull from database
import sqlite3
import json

''' Populating jeopardy trivia questions from data set. '''
conn = sqlite3.connect('trivia.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS trivia')

c.execute('''CREATE TABLE trivia
             (q_id INTEGER PRIMARY KEY NOT NULL, question text, answer text, category text, value integer)''')


trivia_question_list = []

with open("jeopardy.json") as json_file:
    json_data = json.load(json_file)
    trivia_question_list = json_data

for q in trivia_question_list:
    question, answer, category, value = q["question"], q["answer"], q["category"], q["value"]
    if (value):
        value = ''.join([i for i in value if i.isalnum()])
    else:
        value = 0
    c.execute('INSERT INTO trivia(question, answer, category, value) VALUES (?, ?, ?, ?)', (question, answer, category, value))

conn.commit()

conn.close()
