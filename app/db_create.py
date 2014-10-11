# db_create.py
from views import db
from models import Task
from datetime import date 

#create db and db table
try:
	db.create_all()
except Error:
	print "SOmething went wrong with db creation"

#insert data
db.session.add(Task("Finish this tutorial", date(2014, 3, 13), 10, 1))
db.session.add(Task("Finish Real Python", date(2014, 3, 13), 10, 1))

print "got to last line"
#commit changes
try:
	db.session.commit()
except Error:
	print "Runtime Error"