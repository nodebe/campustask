from flask import Blueprint
from flask_login import login_required


users = Blueprint('users', __name__)


@login_required
@users.route('/user_dashboard')
def user_dashboard():

	return "<h1>User dashboard</h1>"
