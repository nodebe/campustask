from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, current_user
from campustask import db
# from campustask.main.routes import CATEGORIES
from campustask.users.forms import Register, ProfileEdit, PasswordChange
from campustask.models import User, get_categories
from passlib.hash import sha256_crypt as sha256


users = Blueprint('users', __name__)
error_message = 'Something went wrong, try again later! '

@users.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('users.user_dashboard'))
	global error_message
	register_form = Register()

	if register_form.validate_on_submit():
		hashed_password = sha256.encrypt(str(register_form.password.data))
		try:
			user = User(username = register_form.username.data, email = register_form.email.data, password = hashed_password)
			db.session.add(user)
			db.session.commit()
			user_login = User.query.filter_by(email=register_form.email.data).first()
			login_user(user_login)
			flash('Account created successfully!', 'success')
			flash('Please complete your profile!','info')
			return redirect(url_for('users.userprofile'))
		except Exception as e:
			flash(error_message + str(e), 'warning')
	

	return render_template('register.html', title = 'Register', categories = get_categories(), form = register_form)

@users.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('users.user_dashboard'))

	return render_template('login.html', title = 'Login')

@users.route('/user_dashboard')
@login_required
def user_dashboard():

	return "<h1>User dashboard</h1>"

@users.route('/userprofile', methods = ['GET', 'POST'])
@users.route('/userprofile/<string:form_type>', methods = ['GET', 'POST'])
@login_required
def userprofile(form_type=''):
	password_form = PasswordChange()
	form = ProfileEdit()

	if request.method == 'GET':
		form.firstname.data = current_user.firstname
		form.lastname.data = current_user.lastname
		form.email.data = current_user.email
		form.campus.data = current_user.campus
		form.phone.data = current_user.phone

	if form_type == 'password' and password_form.validate_on_submit():
		try:
			current_user.password = sha256.encrypt(str(password_form.newpassword.data))
			db.session.commit()
			flash('Password changed successfully', 'success')
		except Exception as e:
			flash(error_message + str(e), 'warning')
		finally:
			return redirect(url_for('users.userprofile'))

	if form_type == 'profile' and form.validate_on_submit():
		try:
			current_user.firstname = form.firstname.data
			current_user.lastname = form.lastname.data
			current_user.phone = form.phone.data
			current_user.campus = form.campus.data
			current_user.email = form.email.data
			db.session.commit()
			flash('Profile updated successfully', 'success')
			return redirect(url_for('users.userprofile'))
		except Exception as e:
			flash(error_message + str(e), 'warning')
			return redirect(url_for('users.userprofile'))

	return render_template('edit-profile.html', title = 'Profile', categories = get_categories(), password_form = password_form, form = form)

'''
@users.route('/passwordchange', methods = ['POST'])
@login_required
def passwordchange():
	form = ProfileEdit()

	password_form = PasswordChange()
	if password_form.validate_on_submit():
		try:
			current_user.password = sha256.encrypt(str(password_form.newpassword.data))
			db.session.commit()
			flash('Password changed successfully', 'success')
		except Exception as e:
			flash(error_message + str(e), 'warning')
		finally:
			return redirect(url_for('users.userprofile'))
	else:
		return redirect(url_for('users.userprofile'))'''