from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from campustask.config import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager =  LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from campustask.models import *


from campustask.users.routes import users
from campustask.main.routes import main
from campustask.task.routes import task

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(task)


@login_manager.user_loader
def load_user(user_id):
	'''This callback is used to reload the user object from the user ID stored in the session. 
	It should take the unicode ID of a user, and return the corresponding user object'''
	
	return User.query.get(int(user_id))


db.create_all()
db.session.commit()