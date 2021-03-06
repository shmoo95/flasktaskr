# db_migrate.py

from views import db
#from datetime import datetime
from config import DATABASE_PATH
import sqlite3

#with sqlite3.connect(DATABASE_PATH) as connection:

	#c = connection.cursor()

	#c.execute("""ALTER TABLE task RENAME TO old_tasks""")

	#db.create_all()

	#c.execute("""ALTER TABLE task RENAME TO tasks""")

	#c.execute("""SELECT name, due_date, priority, status FROM old_tasks ORDER BY task_id ASC""")

	#data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in c.fetchall()]

	#c.executemany("""INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id) VALUES (?,?,?,?,?,?)""", data)

	#c.execute("DROP TABLE old_tasks")

with sqlite3.connect(DATABASE_PATH) as connection:

	c = connection.cursor()

	c.execute("""ALTER TABLE users RENAME TO old_users""")

	db.create_all()

	c.execute("""SELECT name, email, password FROM old_users ORDER BY id ASC""")

	data = [(row[0], row[1], row[2], 'user') for row in c.fetchall()]

	c.executemany("""INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)""", data)

	c.execute("DROP TABLE old_users")