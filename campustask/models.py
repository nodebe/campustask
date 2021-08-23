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

task_to_category = db.Table('task_to_category',
	db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
	db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
	)

task_to_subcategory = db.Table('task_to_subcategory',
	db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
	db.Column('subcategory_id', db.Integer, db.ForeignKey('subcategory.id'))
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
	#link to the user_to_task table
	tasks_subscribed = db.relationship('Task', secondary=user_to_tasks, backref = db.backref('task_subscribed_to', lazy='dynamic'))


class Task(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	#connects to the user model to the agent that owns the task
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(150), nullable = False)
	#Days Until Delivery of service
	d_u_d = db.Column(db.Integer, nullable = False)
	price = db.Column(db.String, nullable = False)
	description = db.Column(db.Text, nullable = False)
	_image_name = db.Column(db.String, default = None)
	image_hash = db.Column(db.Text)
	#connects to the plan model, a task can have only one plan
	plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
	#number of times the task has been completed by the agent
	times_completed = db.Column(db.Integer, default = 0)
	#_rating = db.Column(db.String, default = '0.0')
	#link to category table
	task_category = db.relationship('Category', secondary=task_to_category, backref = db.backref('task_head_category', lazy='dynamic'))
	#link to subcategory table
	task_sub_category = db.relationship('Subcategory', secondary=task_to_subcategory, backref = db.backref('task_subcategory', lazy='dynamic'))
	views = db.Column(db.Integer, default = 0)


	'''@property
				def rating(self):
			
					return [float(x) for x in self._rating.split(';')]
				
				@rating.setter
				def rating(self, value):
					self._ratings += ';{}'.format(value)'''


	@property
	def image_name(self):

		return [image for image in self._image_name.split(';')]

	@image_name.setter
	def image_name(self, images):
		for image in images:
			if self._image_name != None:
				self._image_name += ';{}'.format(image)
			else:
				self._image_name = '{}'.format(image)


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


class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	name = db.Column(db.String())
	#one category can have many subcategories
	sub_categories = db.relationship('Subcategory', backref = 'category_sub')

class Subcategory(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique = True)
	name = db.Column(db.String())
	#connects to the category model
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


def get_categories():
	'''
	This creates and sends categories to pages that need to display them
	'''
	db_categories = Category.query.all()

	categories = {}

	for i in db_categories:
		categories[i.name] = [x.name for x in i.sub_categories]

	return categories
