from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, MultipleFileField
from flask_wtf.file import FileAllowed
from wtforms.fields import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange


class TaskPost(FlaskForm):
	title = StringField('Title: *', validators = [InputRequired(''), Length(max = 90)])
	d_u_d = IntegerField('Days until Delivery: *', validators = [InputRequired(), NumberRange(min=1)])
	price = IntegerField('Price: *', validators = [InputRequired()])
	description = TextAreaField('Service Description: *', validators = [InputRequired()])
	# categories = BooleanField()
	images = MultipleFileField('Images: ', validators = [FileAllowed(['jpg','png', 'jpeg','JPG','JPEG','PNG'])])
