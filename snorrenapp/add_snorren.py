import mtcnn
import matplotlib.pyplot as plt
from PIL import Image
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from flask import jsonify


@dataclass
class Coordinate():
    """The coordinates of a point in a picture with (0, 0) being
    the top left corner
    """
    x: int
    y: int
    

@dataclass
class FaceKeypoints():
    """Relevant results of face recognition model for SnorrenTijd"""
    mouth_left: Coordinate
    mouth_right: Coordinate
    nose: Coordinate


@dataclass
class LipBoxData():
    """Information for the holding place of the snor"""
    top_position: Coordinate
    dx: int
    dy: int
    angle: int = None

    def __repr__(self):
        dict_to_print = {
            'x': self.top_position.x,
            'y': self.top_position.y,
            'width': self.dx,
            'height': self.dy,
            'angle': self.angle
        }
        return str(dict_to_print)


class UpperLipBox():
    """Data about the location where the snor should be attached to the face. It's the 'box'
    between the upper lip and nose, a.k.a. the base of the snor
    """
    def __init__(self,
                 facekey_points: FaceKeypoints,
                 lipbox: LipBoxData = None):

    @staticmethod
    def define_snor_size(face_keypoints: FaceKeypoints) -> Tuple[int, int]:
        width = face_keypoints.mouth_right.x - face_keypoints.mouth_left.x

        max_lips = max(face_keypoints.mouth_right.y, face_keypoints.mouth_left.y)
        height = max_lips - face_keypoints.nose.y
        return width, height

    @staticmethod
    def define_snor_position(face_keypoints: FaceKeypoints) -> Tuple[int, int, int]:
        """The top left coordinates are the top left point of the snor. It is positioned
        between the mouth and nose of the person."""

        dx = face_keypoints.mouth_right.x - face_keypoints.mouth_left.x
        x = face_keypoints.nose.x - math.floor(dx/2)

        y_mouth = min(face_keypoints.mouth_left.y, face_keypoints.mouth_right.y)
        dy = y_mouth - face_keypoints.nose.y
        y = face_keypoints.nose.y + math.floor(dy*0.3)

        angle = math.degrees(math.tan(dx/dy))
        return x, y, angle

    def calculate_lip_box(self):
        """Calculates the lipbox based on the face_keypoints attribute"""
        width, height = define_snor_size()
        x, y, angle = define_snor_position()
        self.lipbox = LipBoxData(top_position=Coordinate(x, y),
                            width=width,
                            height=height,
                            angle=angle)

def get_facial_data_response():
    pass


def coordinate_from_tuple(coordinates: Tuple) -> Coordinate:
    """Transforms a tuple format to an x, y Coordinate object."""
    coordinate = Coordinate(coordinates[0], coordinates[1])
    return coordinate





def get_facial_keypoints(image_path: str, 
                         detect_local: bool,
                         location: str = None) -> List[Dict[str, int]]:
    """
    Detects faces and returns the coordinates of the box between 
    mouth corners and nose. A list of dictionaries entries per face.
    """
    if detect_local:
        response = detect_faces_local(image_path)
    else:
        response = detect_faces_external(image_path, location)

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


def detect_faces_local(image_path: str) -> str:
    """When run locally this calculates the face postitions.
    If run in seperate containers, this is the response from the ML server

    The return is a JSON in the same format as the web ML model would provide"""
    # Maybe better to pass a detector as an argument
    detector = mtcnn.MTCNN()
    faces = detector.detect_faces(plt.imread(image_path))
    response = jsonify(faces)
    return response


def detect_faces_external(image_path: str, location: str) -> str:
    pass

