from campustask.models import User
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.fields import EmailField, TelField, URLField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from campustask.users.config import campus_choice
from passlib.hash import sha256_crypt as sha256


class Register(FlaskForm):
	username = StringField('Username:', validators = [InputRequired('Fill in a username'), Length(min = 3,max = 10)] )
	email = EmailField('Email:', validators = [InputRequired('Fill in a valid Email')])
	password = PasswordField('Password:', validators = [InputRequired('Fill in a strong password'), Length(min = 6, message = 'Password must be more than 6 characters')])
	confirm = PasswordField('Repeat Password:', validators = [EqualTo('password', message = 'Passwords must match')])
	agree = BooleanField('', validators = [InputRequired()], default='checked')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('Email already exists!')

class ProfileEdit(FlaskForm):
	firstname = StringField('Firstname:')
	lastname = StringField('Lastname:')
	email = EmailField('Email:', validators = [InputRequired('Fill in a valid Email')])
	phone = TelField('Phone Number:')
	campus = SelectField('Campus:', choices=campus_choice)
	bio = TextAreaField('Bio:', validators = [Length(max = 300)])
	facebook = StringField('Facebook id:')
	website = URLField('Website:')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('Email already exists!')

class PasswordChange(FlaskForm):
	oldpassword = PasswordField('Old Password:', validators = [InputRequired()])
	newpassword = PasswordField('Password:', validators = [InputRequired('Fill in a strong password'), Length(min = 6, message = 'Password must be more than 6 characters')])
	confirm = PasswordField('Repeat Password:', validators = [EqualTo('newpassword', message = 'Passwords must match')])


	def validate_oldpassword(self, oldpassword):
		if not sha256.verify(oldpassword.data, current_user.password):
			raise ValidationError('Password is not correct!')