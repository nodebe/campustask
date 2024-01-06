from flask import Blueprint, render_template, flash
from campustask.models import get_categories
#from campustask.models import *

main = Blueprint('main', __name__)


#CATEGORIES = {'Advertising': ['Banner Advertising', 'Flyers & Handouts', 'Hold Your Sign', 'Human Billboards', 'Music Promotion', 'Other', 'Outdoor Advertising', 'Pet Models', 'Radio'],'Business':['Branding Services', 'Business Plans', 'Business Tips', 'Career Advice', 'Financial Consulting', 'Legal Consulting', 'Market Research', 'Other', 'Presentations', 'Virtual Assistant'], 'Graphics & Design':['Architecture', 'Banners & Headers', 'Business Cards', 'Cartoons & Caricatures', 'Ebook Covers & Packages', 'Flyers & Brochures', 'Illustration', 'Landing Pages', 'Logo Design', 'Other'], 'Music & Audio':['Audio Editing & Mastering', 'Custom Ringtones', 'Custom Songs', 'Hip-Hop Music', 'Jingles', 'Music Lessons', 'Narration & Voice-Over', 'Other', 'Rap Music', 'Songwriting'], 'Online Marketing':['Article & PR Submission', 'Blog Mentions', 'Bookmarking & Links', 'Domain Research', 'Fan Pages', 'Get Traffic', 'Keywords Research', 'Other', 'SEO', 'Social Marketing'], 'Programming & Tech':['.Net', 'C++', 'CSS & HTML', 'Databases', 'iOS, Android & Mobile', 'Java', 'JavaScript', 'Joomla & Drupal', 'Other', 'PHP'], 'Video & Animation':['Animation & 3D', 'Commercials', 'Editing & Post Production', 'Intros', 'Other', 'Puppets', 'Stop Motion', 'Testimonials & Reviews by Actors'], 'Writing & Translation': ['Copywriting', 'Creative Writing & Scripting', 'Other', 'Press Releases', 'Proofreading & Editing', 'Resumes & Cover Letters', 'Reviews', 'SEO Keyword Optimization', 'Speech Writing', 'Transcripts']}


@main.route('/')
def index():

	return render_template('home.html', categories=get_categories(), title='Home')


@main.route('/parent_category/<string:parent_category>')
def parent_category(parent_category):

	return "<h1>This is to display services that have parent category {}</h1>".format(parent_category)

@main.route('/child_category/<string:child_category>')
def child_category(child_category):

	return "<h1>This is to display services that have child category {}</h1>".format(child_category)