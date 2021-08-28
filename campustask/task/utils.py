import os
import secrets
from PIL import Image
from campustask.config import app
import base64
from resizeimage import resizeimage

def save_picture(form_picture):
	picture_fn = []

	for i in form_picture:
		random_hex = secrets.token_hex(8)
		_, f_ext = os.path.splitext(i.filename)
		pic_name = random_hex + f_ext
		picture_fn.append(pic_name)
		picture_path_normal = os.path.join(app.root_path, "static/img/tasks/normal", pic_name)
		picture_path_slides = os.path.join(app.root_path, "static/img/tasks/slides", pic_name)

		j = Image.open(i) 
		k = Image.open(i)
		j = resizeimage.resize_cover(j, [180, 180], validate=False)
		k = resizeimage.resize_cover(j, [870, 489], validate=False)
		j.save(picture_path_normal)
		k.save(picture_path_slides)

	return picture_fn

def delete_picture(pic_name_list):
	for i in pic_name_list:
		print(i)
		picture_path_normal = os.path.join(app.root_path, 'static/img/tasks/normal', i)
		picture_path_slides = os.path.join(app.root_path, 'static/img/tasks/slides', i)
		os.remove(picture_path_normal)
		os.remove(picture_path_slides)