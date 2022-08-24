import secrets
from pathlib import Path
import time
from datetime import date
import logging
from flask import render_template, send_from_directory, request, jsonify
from snorrenapp import app
from snorrenapp.add_snorren import get_facial_keypoints


logger = logging.getLogger(__name__)


def save_picture(form_picture) -> str:
    """Save a picture locally"""
    random_hex = secrets.token_hex(8)
    f_ext = Path(form_picture.filename).suffix
    # _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    picture_path = Path(app.config["IMAGE_UPLOADS"], picture_fn)
    print(picture_path)
    form_picture.save(picture_path)
    return picture_fn


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    """Returns a rendered homepage."""
    return render_template('home.html', current_year=date.today().year)


@app.route('/uploadImage', methods=["GET", 'POST'])
def upload_image():
    """Generates a response with the facial feature coordinates as present in a picture."""

    isthisfile = request.files.get('file')
    save_fn = Path(app.config["IMAGE_UPLOADS"], isthisfile.filename)
    isthisfile.save(save_fn)

    tic = time.perf_counter()
    face_coordinates = get_facial_keypoints(save_fn, detect_local=True)
    toc = time.perf_counter()
    print(face_coordinates)
    logging.info(f'Ran facial recognisition on {save_fn}. Found {len(face_coordinates)} in {round(toc-tic,2)} sec')
    
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
    """Route to display a file previously uploaded"""
    return send_from_directory(directory=app.config["IMAGE_UPLOADS"], path=uploaded_image)


@app.route("/about")
def about():
    """Returns the about-page html template"""
    return render_template('about.html', title='About', current_year=date.today().year)
