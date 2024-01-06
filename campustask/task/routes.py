from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from campustask import db
from campustask.models import User, get_categories, Task, Category, Subcategory
# from campustask.main.routes import CATEGORIES
from campustask.task.forms import TaskPost
from campustask.task.utils import save_picture, delete_picture

task = Blueprint('task', __name__)
error_message = 'Something went wrong, try again later! '
recent_tasks = Task.query.all()[::-1][:3]

@task.route('/add_service', methods=['GET', 'POST'])
@task.route('/add_service/<task_id>', methods=['GET', 'POST'])
@login_required
def add_service(task_id=''):
	form = TaskPost()
	category = []
	sub_category = []
	if form.validate_on_submit():
		if task_id == '':
			print(task_id)
			try:
				task = Task(user_id=current_user.id, title=form.title.data, d_u_d=form.d_u_d.data, price=form.price.data, description=form.description.data)
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
				if form.images.data[0].filename != '':
					pictures = save_picture(form.images.data)
					task.image_name=pictures
				else:
					task.image_name = ['default.PNG']
				db.session.commit()
				flash('Task successfully added.','success')
				return redirect(url_for('task.add_service'))
		elif task_id != '':
			# Insert adding of form fields to db
			try:
				task = Task.query.get_or_404(task_id)
				print(form.images.data[0].filename)
				task.title = form.title.data
				task.d_u_d = form.d_u_d.data
				task.price = form.price.data
				task.description = form.description.data
				category_list = request.form.getlist('header')
				current_category_list = [x.name for x in task.task_category]
				sub_category_list = request.form.getlist('subheader')
				current_sub_category_list = [x.name for x in task.task_sub_category]
				# Changing the category of the task from the relationship table
				if category_list != current_category_list and category_list != []:
					for category in current_category_list:
						if category in category_list:
							continue
						else:
							cat = Category.query.filter_by(name=category).first()
							cat.task_head_category.remove(task)
					for category in category_list:
						cat = Category.query.filter_by(name=category).first()
						cat.task_head_category.append(task)
				# Changing the sub category of the task from the relationship table
				if sub_category_list != current_sub_category_list and sub_category_list != []:
					for category in current_sub_category_list:
						if category in sub_category_list:
							continue
						else:
							cat = Subcategory.query.filter_by(name=category).first()
							cat.task_subcategory.remove(task)
					for category in sub_category_list:
						cat = Subcategory.query.filter_by(name=category).first()
						cat.task_subcategory.append(task)

			except Exception as e:
				flash(error_message + str(e), 'warning')
			else:
				if form.images.data[0].filename != '':
					delete_picture(task.image_name)
					pictures = save_picture(form.images.data)
					task.image_name=pictures
				db.session.commit()
				flash('Task successfully edited.','success')
				return redirect(url_for('task.add_service', task_id=task.id))
	elif request.method == 'GET' and task_id!='':
		task = Task.query.get_or_404(task_id)
		if task.user_tasks_owned == current_user:
			form.title.data = task.title
			form.d_u_d.data = task.d_u_d
			form.price.data = task.price
			form.description.data = task.description
			category = [x.name for x in task.task_category]
			sub_category = [x.name for x in task.task_sub_category]
		else:
			print('You are aborted')
			abort(403)

	return render_template('add-service.html', title='Add service', categories=get_categories(), form=form, recent_tasks=recent_tasks, category=category, sub_category=sub_category)

@task.route('/view_service/<service_id>')
def view_service(service_id):
	task = Task.query.filter_by(id=service_id).first()
	if current_user.is_authenticated and task.user_tasks_owned != current_user:
		task.views += 1
		db.session.commit()

	return render_template('view_service.html', title=task.title, task=task)

@task.route('/view_all_service/<user_id>')
def view_all_service(user_id):
	user = User.query.filter_by(id=user_id).first()
	

	return render_template('view_all_service.html', title=f'All tasks by {user.username}', recent_tasks=recent_tasks, user=user, categories=get_categories())


@task.route('/service_payment_description')
def service_payment_description():
	return "Description on different payment plans. <a href='/add_service'> Continue</a>"