from campustask import db, login_manager
#from campustask.utils import unique_id
from flask_login import UserMixin


#this is the relationship table for the user who subscribes/pays for a task
user_to_tasks = db.Table('user_to_tasks',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
	db.Column('status', db.String),
	db.Column('review', db.String),
	db.Column('rating', db.Float, default = 0.0)
	)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	firstname = db.Column(db.String(30))
	lastname = db.Column(db.String(30))
	username = db.Column(db.String(20), nullable = False)
	email = db.Column(db.String(50), nullable = False, unique = True)
	phone = db.Column(db.String(15))
	password = db.Column(db.String(150), nullable = False)
	campus = db.Column(db.String(100))
	no_of_tasks_at_hand = db.Column(db.Integer, default = 0)
	user_status = db.Column(db.String(10), default = 'member')
	#one user can have many notifications
	notifications = db.relationship('Notification', backref = 'user_notifications')
	#one user can have many tasks
	tasks_owned = db.relationship('Task', backref = 'user_tasks_owned')


class Task(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	#connects to the user model to the agent that owns the task
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(150), nullable = False)
	#Days Until Delivery of service
	d_u_d = db.Column(db.Integer, nullable = False)
	price = db.Column(db.String, nullable = False)
	description = db.Column(db.Text, nullable = False)
	_categories = db.Column(db.String, default = "")
	image_name = db.Column(db.String, default = 'default_image.jpg')
	image_hash = db.Column(db.Text)
	#connects to the plan model, a task can have only one plan
	plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
	#number of times the task has been completed by the agent
	times_completed = db.Column(db.Integer, default = 0)
	_rating = db.Column(db.String, default = '0.0')

	@property
	def categories(self):
		#this returns the _categories column as a list to our backend
		return [x for x in self._categories.split(',')]

	@categories.setter
	def categories(self, value):
		#this takes in a list stored as 'value' from the backend and inserts it into the _categories column
		for x in value:
			if self._categories != "":
				self._categories += ',{}'.format(x)
			else:
				self._categories += '{}'.format(x)

	@property
	def rating(self):

		return [float(x) for x in self._rating.split(',')]
	
	@rating.setter
	def rating(self, value):
		self._ratings += ';{}'.format(value)


class Plan(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	title = db.Column(db.String, nullable = False)
	price = db.Column(db.String, nullable = False)
	duration = db.Column(db.String, nullable = False)
	#connects to the task model, a plan can have multiple tasks
	task_id = db.relationship('Task', backref = 'plan_tasks_owned')


class Blog(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	title = db.Column(db.String, nullable = False)
	post = db.Column(db.Text, nullable = False)
	views = db.Column(db.Integer, default = 0)


class Notification(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	message = db.Column(db.Text, nullable = False)
	#connects to the user model
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Contact(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	firstname = db.Column(db.String(30), nullable = False)
	lastname = db.Column(db.String(30))
	email = db.Column(db.String(50), nullable = False, unique = True)
	message = db.Column(db.Text, nullable = False)
	read = db.Column(db.Integer, default = 0)

