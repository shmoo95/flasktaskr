#views.py

from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from forms import AddTaskForm, RegisterForm, LoginForm





app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Task, User


def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('You are logged out. Bye. :(')
	return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
	error= None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			u = User.query.filter_by(
				name=request.form['name'],
				password=request.form['password']).first()
			if u is None:
				error = 'Invalid Username or password'
				return render_template(
					"login.html",
					form=form,
					error=error)
			else:
				session['logged_in'] = True
				flash('You are logged in. Go Crazy')
				return redirect(url_for('tasks'))
		else:
			return render_template(
				"login.html",
				form=form,
				error=error
				)
	if request.method == 'GET':
		return render_template('login.html', form=form)

@app.route('/tasks/')
@login_required
def tasks():
	open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
	closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())
	return render_template(
		'tasks.html',
		form=AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
		)

@app.route('/add/', methods=['POST'])
@login_required
def new_task():
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		
		if form.validate_on_submit():
			print "Got past validate"
			new_task = Task(
				form.name.data,
				form.due_date.data,
				form.priority.data,
				'1')
			
			db.session.add(new_task)
			db.session.commit()

			flash('New entry was successfully posted. Thanks.')
	return redirect(url_for('tasks'))

#mark tasks as complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	new_id = task_id
	db.session.query(Task).filter_by(task_id = new_id).update({"status": "0"})
	db.session.commit()
	flash('The task was marked as complete.')
	return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
	new_id = task_id
	db.session.query(Task).filter_by(task_id=new_id).delete()
	db.session.commit()
	flash('The task was deleted. Why not add a new one?')
	return redirect(url_for('tasks'))

# User Registration
@app.route('/register/', methods=['GET', 'POST'])
def register():
	print "GOt to Register"
	error = None
	form= RegisterForm(request.form)
	if request.method == 'POST':
		print "GOt to Post1"
		if form.validate_on_submit():
			print "GOt to Post"
			new_user = User(
				form.name.data,
				form.email.data,
				form.password.data,
				)
			print "GOt to Commit"
			db.session.add(new_user)
			db.session.commit()
			flash('Thanks for registering. Please login')
			return redirect(url_for('login'))
		else:
			return render_template('register.html', form=form, error=error)
	if request.method == 'GET':
		return render_template('register.html', form=form)

