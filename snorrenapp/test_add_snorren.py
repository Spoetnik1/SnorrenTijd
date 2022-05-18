import unittest
from add_snorren import FaceKeypoints, UpperLipBox
from snorrenapp import app


class SnorRecognitionTests(unittest.TestCase):
    """Look at ddt: https://ddt.readthedocs.io/en/latest/example.html. Model result
    show some variance thus testing requires certain ranges instead of exact int matches."""

    def test_UpperLipBox_creation(self):
        # Based on test photo, nana_without_snor.jpg

        # Some flask context creation
        ctx = app.app_context()
        ctx.push()
        with ctx:
            face_data = {'nose': (621, 832),
                         'mouth_left': (579, 887),
                         'mouth_right': (677, 887)}

            face_keypoints = FaceKeypoints.from_dict(face_data)
            lip_box = UpperLipBox(face_keypoints)
            response_dict = lip_box.get_lip_box()
            if 'angle' in response_dict:
                response_dict.pop('angle')

            expected_reply = {
                "x": 572,
                "y": 848,
                "height": 55,
                "width": 98
            }
            self.assertEqual(expected_reply, response_dict)


if __name__ == '__main__':
    unittest.main()
