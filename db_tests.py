import sqlite3

def trivia_tests():
    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM trivia')
    print c.fetchone()[0]

    test_id = 1

    c.execute('SELECT * FROM trivia WHERE q_id=?', (test_id,))
    print c.fetchone()

    conn.close()

def amc8_tests():
    conn = sqlite3.connect('amceight.db')
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM amceight')
    print c.fetchone()[0]

    test_id = 1

    c.execute('SELECT * FROM amceight WHERE q_id=?', (test_id,))
    print c.fetchone()

    conn.close()

trivia_tests()
amc8_tests()
