# Want to let bot pull from database
import sqlite3
import json

def populate_trivia():
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

def populate_amc8():
    # Populate AMC8 DB
    conn = sqlite3.connect('amceight.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS amceight')
    c.execute('''CREATE TABLE amceight
                 (q_id INTEGER PRIMARY KEY NOT NULL, question text, answer text, category text, value integer)''')

    baselink = "https://hidden-spire-42316.herokuapp.com/amc8/"
    amc8_question_list = []


    with open("amc8.json") as json_file:
        json_data = json.load(json_file)
        amc8_question_list = json_data

    for q in amc8_question_list:
        question_no, answer, category, year = q["question"], q["answer"], q["category"], q["year"]
        value = int(question_no)*100
        question = baselink + year + "problem" + question_no + ".png"
        c.execute('INSERT INTO amceight(question, answer, category, value) VALUES (?, ?, ?, ?)', (question, answer, category, value))

    conn.commit()
    conn.close()

populate_trivia()
populate_amc8()
