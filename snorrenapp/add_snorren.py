import mtcnn
import matplotlib.pyplot as plt
from PIL import Image
import math
from typing import Dict


def define_snor_size(face_keypoints):
    width = face_keypoints['mouth_right'][0] - face_keypoints['mouth_left'][0]

    max_lips = max(face_keypoints['mouth_right'][1], face_keypoints['mouth_left'][1])
    height = max_lips - face_keypoints['nose'][1]

    return width, height


def define_snor_position(face_keypoints):
    """The top left coordinates are the top left point of the snor. It is positioned
    between the mouth and nose of the person."""

    dx = face_keypoints['mouth_right'][0] - face_keypoints['mouth_left'][0]
    x = face_keypoints['nose'][0] - math.floor(dx/2)

    y_mouth = min(face_keypoints['mouth_left'][1], face_keypoints['mouth_right'][1])
    dy = y_mouth - face_keypoints['nose'][1]
    y = face_keypoints['nose'][1] + math.floor(dy*0.3)

    angle = math.degrees(math.tan(dx/dy))
    return x, y, angle


def get_facial_keypoints(image_path: str) -> Dict[str, int]:
    """
    Detects faces and returns the coordinates of the box between mouth corners and nose. A list of dictionaries entries per face.
    """
    detector = mtcnn.MTCNN() # Maybe better to pass as an argument, for when the server is always running
    faces = detector.detect_faces(plt.imread(image_path))

    face_keypoints = []
    for face in faces:
        new_face = {}

        x, y, angle = define_snor_position(face['keypoints'])
        new_face['x'] = x
        new_face['y'] = y
        new_face['angle'] = round(angle, 2)

        width, height = define_snor_size(face['keypoints'])
        new_face['width'] = width
        new_face['height'] = height

        face_keypoints.append(new_face)
    return face_keypoints


def draw_snorren(orginal_image_path: str, snor_path: str):
    """Takes an image to fit snorren to, and a snor to fit. Saves an image with the snorren placed in the picture."""

    detector = mtcnn.MTCNN() # Maybe better to pass as an argument, for when the server is always running
    faces = detector.detect_faces(plt.imread(orginal_image_path))

    initial_snor = Image.open(snor_path).convert("RGBA")
    image_to_snor = Image.open(orginal_image_path).convert("RGBA")

    for face in faces:
        snor_size = define_snor_size(face['keypoints'])
        snor_position, angle = define_snor_position(face['keypoints'])

        snor_resized = initial_snor.copy()
        snor_resized = snor_resized.resize(snor_size)
        #snor_resized = snor_resized.rotate(angle, Image.NEAREST, expand = 1)

        image_to_snor.paste(snor_resized, snor_position)#, mask=snor_resized)

    imaged_snorred = image_to_snor.convert('RGB')
    return imaged_snorred
