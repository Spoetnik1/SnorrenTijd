from __future__ import annotations
import mtcnn
import matplotlib.pyplot as plt
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Coordinate:
    """The coordinates of a point in a picture with (0, 0) being
    the top left corner
    """
    x: int
    y: int

    @classmethod
    def from_tuple(cls, coordinate_tuple: Tuple) -> Coordinate:
        return cls(coordinate_tuple[0], coordinate_tuple[1])

    @classmethod
    def from_list(cls, coordinate_list: List) -> Coordinate:
        return cls(coordinate_list[0], coordinate_list[1])


@dataclass
class FaceKeypoints:
    """Relevant results of face recognition model for SnorrenTijd"""
    mouth_left: Coordinate
    mouth_right: Coordinate
    nose: Coordinate

    @classmethod
    def from_dict(cls, face_keypoints_dict: Dict[str, Tuple[int, int]]) -> FaceKeypoints:
        mouth_left = Coordinate.from_tuple(face_keypoints_dict['mouth_left'])
        mouth_right = Coordinate.from_tuple(face_keypoints_dict['mouth_right'])
        nose = Coordinate.from_tuple(face_keypoints_dict['nose'])
        return cls(mouth_left=mouth_left, mouth_right=mouth_right, nose=nose)


@dataclass
class LipBoxData:
    """Information for the holding place of the snor"""
    top_position: Coordinate
    dx: int
    dy: int
    angle: int = None

    def response_dict(self):
        lip_box_dict = {
            'x': self.top_position.x,
            'y': self.top_position.y,
            'width': self.dx,
            'height': self.dy,
            'angle': self.angle
        }
        return lip_box_dict


class UpperLipBox:
    """Data about the location where the snor should be attached to the face. It's the 'box'
    between the upper lip and nose, a.k.a. the base of the snor
    """
    def __init__(self, face_keypoints: FaceKeypoints, upper_lip_box: LipBoxData = None):
        self.face_keypoints = face_keypoints
        self.upper_lip_box = upper_lip_box
        if upper_lip_box is None:
            self.calculate_lip_box(self.face_keypoints)

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
        x = int(math.floor(face_keypoints.nose.x - (dx/2)))

        y_mouth = min(face_keypoints.mouth_left.y, face_keypoints.mouth_right.y)
        dy = y_mouth - face_keypoints.nose.y
        y = face_keypoints.nose.y + math.floor(dy*0.3)

        angle = int(math.degrees(math.tan(dx/dy)))
        return x, y, angle

    def calculate_lip_box(self, face_kepoints):
        """Calculates the lipbox based on the face_keypoints attribute"""
        width, height = self.define_snor_size(face_kepoints)
        x, y, angle = self.define_snor_position(face_kepoints)
        self.upper_lip_box = LipBoxData(top_position=Coordinate(x, y),
                                        dx=width,
                                        dy=height,
                                        angle=angle)

    def get_lip_box(self):
        if self.upper_lip_box is not None:
            return self.upper_lip_box.response_dict()
        else:
            raise AttributeError("Calculate lipbox first")


def get_facial_keypoints(image_path: str,
                         detect_local: bool,
                         location: str = None) -> List[Dict[str, int]]:
    """ Detects faces and returns the coordinates of the box between
    mouth corners and nose. A list of dictionaries entries per face.
    """
    if detect_local:
        faces = detect_faces_local(image_path)
    else:
        faces = detect_faces_external(image_path, location)

    lip_boxen = []
    for face in faces:
        face_keypoints = FaceKeypoints.from_dict(face)
        lip_box = UpperLipBox(face_keypoints)
        lip_boxen.append(lip_box.get_lip_box())
    return lip_boxen


def detect_faces_local(image_path: str) -> List[Dict[str, Tuple[int, int]]]:
    """When run locally this calculates the face postitions.
    If run in seperate containers, this is the response from the ML server

    The return is a JSON in the same format as the web ML model would provide"""
    # Maybe better to pass a detector as an argument
    detector = mtcnn.MTCNN()
    faces = detector.detect_faces(plt.imread(image_path))
    faces_list = []
    for face in faces:
        faces_list.append(face['keypoints'])
    return faces_list


def detect_faces_external(image_path: str, location: str) -> str:
    pass
