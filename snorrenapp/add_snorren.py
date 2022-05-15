import mtcnn
import matplotlib.pyplot as plt
from PIL import Image
import math
from typing import Dict, List
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
class FaceKeypoint():
    """Relevant results of face recognition model for SnorrenTijd"""
    mouth_left: Coordinate
    mouth_right: Coordinate
    nose: Coordinate
    

class UpperLipBox():
    """Data about the location where the snor should be attached to the face. It's the 'box'
    between the upper lip and nose, a.k.a. the base of the snor
    """
    def __init__(self, facekeypoints: FaceKeypoint):
        self.facekeypoints = facekeypoints
        self.define_snor_size()
        self.define_snor_position()
        
    def define_snor_size(self):
        """Defines the width and height of the lip box"""
        self.width = self.facekeypoints.mouth_right.x - self.facekeypoints.mouth_left.x
        max_lips = max(self.facekeypoints.mouth_right.y, self.facekeypoints.mouth_left.y)
        self.height = max_lips - self.facekeypoints.nose.y
        
    def define_snor_position(self):
        """Defines the position and angle of the lip box"""
        dx = self.facekeypoints.mouth_right.x - self.facekeypoints.mouth_left.x
        x = self.facekeypoints.nose.x - math.floor(dx/2)
        
        y_mouth = min(self.facekeypoints.mouth_left.y, self.facekeypoints.mouth_right.y)
        dy = y_mouth - self.facekeypoints.nose.y
        
        angle = math.degrees(math.tan(dx/dy))
        
        self.coordinate = Coordinate(x, y)
        self.angle = math.degrees(math.tan(dx/dy))
        
    def response():
        """Generates a dictionary that could be used as a payload to the client"""
        response = {}
        return response
            

        
 
        
        
        
        


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
