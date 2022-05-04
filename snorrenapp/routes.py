from snorrenapp import app
from snorrenapp.forms import PictureSubmitForm
from snorrenapp.add_snorren import get_facial_keypoints
from flask import render_template, flash, url_for, redirect, send_from_directory, abort, session, request, jsonify, g
import secrets
import os
import time


def resize_picture(form_picture):
    pass


def save_picture(form_picture):
    """Save a picture locally"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = f"C://Users//super//IdeaProjects//snorren//snorrenapp//static//uploaded_images//{picture_fn}"
    form_picture.save(picture_path)
    return picture_fn


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# def home():
#     form = PictureSubmitForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_fn = save_picture(form.picture.data)
#             session['uploaded_image'] = picture_fn
#             print(session['uploaded_image'])
#             flash('Your imaged has been saved!', 'success')
#             return render_template('home.html', form=form, uploaded_image=picture_fn)
#         else:
#             flash('No image sumbitted, please try again', 'warning')
#     return render_template('home.html', form=form)


# @app.route("/withajax2", methods=['GET', 'POST'])
# @app.route("/", methods=['GET', 'POST'])
# @app.route("/home", methods=['GET', 'POST'])



@app.route('/uploadImage', methods=["GET", 'POST'])
def upload_image():
    IMAGE_PATH = "C://Users//super//IdeaProjects//snorren//snorrenapp//static//uploaded_images//"

    isthisFile = request.files.get('file')
    save_fn = IMAGE_PATH + isthisFile.filename
    isthisFile.save(save_fn)

    face_coordinates = get_facial_keypoints(save_fn)
    print(face_coordinates)
    if len(face_coordinates) < 1:
        response = jsonify(
            message='No faces detected',
            category='success',
            status=200
        )
        return response

    response = jsonify(
        message=f'Found {len(face_coordinates)} face(s)!',
        faceData=face_coordinates,
        category="success",
        status=200
    )
    return response


@app.route('/get_image/<uploaded_image>')
def display_uploaded_file(uploaded_image):
    return send_from_directory(directory=app.config["IMAGE_UPLOADS"], path=uploaded_image)


@app.route("/about")
def about():
    return render_template('about.html', title='About')
