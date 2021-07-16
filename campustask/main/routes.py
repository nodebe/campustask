from flask import Blueprint, render_template, flash
#from campustask.models import *

main = Blueprint('main', __name__)


@main.route('/')
def index():

	flash('It is working', 'success')
	return render_template('layout.html')