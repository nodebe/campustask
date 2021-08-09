from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from campustask import db
from campustask.models import User, get_categories, Task, Category, Subcategory
# from campustask.main.routes import CATEGORIES
from campustask.task.forms import TaskPost
from campustask.task.utils import save_picture, delete_picture

task = Blueprint('task', __name__)
error_message = 'Something went wrong, try again later! '


@task.route('/add_service', methods = ['GET', 'POST'])
@login_required
def add_service():
	form = TaskPost()
	if form.validate_on_submit():
		if form.images.data != []:
			pictures = save_picture(form.images.data)
		else:
			pictures = ['default.PNG']
		try:
			task = Task(user_id = current_user.id, title = form.title.data, d_u_d = form.d_u_d.data, price = form.price.data, description = form.description.data, image_name=pictures)
			db.session.add(task)
			db.session.commit()
			# Adding the category to task into relationship table
			if request.form.getlist('header') != []:
				for category in request.form.getlist('header'):
					cat = Category.query.filter_by(name=category).first()
					cat.task_head_category.append(task)
			if request.form.getlist('subheader')  != []:
				for category in request.form.getlist('subheader'):
					cat = Subcategory.query.filter_by(name=category).first()
					cat.task_subcategory.append(task)
			db.session.commit()

			flash('Task successfully added.','success')
			return redirect(url_for('task.add_service'))
		except Exception as e:
			if pictures != ['default.PNG']:
				delete_picture(pictures)
			flash(error_message + str(e), 'warning')

	return render_template('add-service.html', title = 'Add service', categories = get_categories(), form = form)

@task.route('/service_payment_description')
def service_payment_description():
	return "Description on different payment plans. <a href='/add_service'> Continue</a>"