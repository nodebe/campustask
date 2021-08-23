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
		try:
			task = Task(user_id = current_user.id, title = form.title.data, d_u_d = form.d_u_d.data, price = form.price.data, description = form.description.data)
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
		except Exception as e:
			flash(error_message + str(e), 'warning')
		else:
			if form.images.data != []:
				pictures = save_picture(form.images.data)
				task.image_name=pictures
			else:
				task.image_name = ['default.PNG']
			db.session.commit()
			flash('Task successfully added.','success')
			return redirect(url_for('task.add_service'))

	return render_template('add-service.html', title = 'Add service', categories = get_categories(), form = form)

@task.route('/view_service/<service_id>')
def view_service(service_id):
	task = Task.query.filter_by(id = service_id).first()
	if current_user.is_authenticated and task.user_tasks_owned != current_user:
		task.views += 1
		db.session.commit()

	return render_template('view_service.html', title = task.title, task = task)

@task.route('/view_all_service/<user_id>')
def view_all_service(user_id):
	user = User.query.filter_by(id = user_id).first()
	recent_tasks = Task.query.all()[::-1][:3]

	return render_template('view_all_service.html', title=f'All tasks by {user.username}', recent_tasks = recent_tasks, user = user, categories = get_categories())


@task.route('/service_payment_description')
def service_payment_description():
	return "Description on different payment plans. <a href='/add_service'> Continue</a>"