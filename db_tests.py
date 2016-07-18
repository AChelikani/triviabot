import sqlite3

conn = sqlite3.connect('trivia.db')
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM trivia')
print c.fetchone()[0]

test_id = 1

c.execute('SELECT * FROM trivia WHERE q_id=?', (test_id,))
print c.fetchone()

conn.close()
