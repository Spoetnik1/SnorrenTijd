import unittest
from snorrenapp.add_snorren import FaceKeypoints, UpperLipBox, coordinate_from_tuple


class MyTestCase(unittest.TestCase):
    """Look at ddt: https://ddt.readthedocs.io/en/latest/example.html. Model result
    show some variance thus testing requires certain ranges instead of exact int matches."""

    def test_UpperLipBox_creation(self):
        # Based on test photo, nana_without_snor.jpg
        facial_data = {'nose': (621, 832),
                       'mouth_left': (579, 887),
                       'mouth_right': (677, 887)}

        mouth_left = coordinate_from_tuple(facial_data['mouth_left'])
        mouth_right = coordinate_from_tuple(facial_data['mouth_right'])
        nose = coordinate_from_tuple(facial_data['nose'])

        test_face = FaceKeypoints(mouth_left=mouth_left,
                                  mouth_right=mouth_right,
                                  nose=nose)
        lip_box = UpperLipBox(test_face)
        lip_box_payload = lip_box.response()

        expected_reply = {
            "height": 55,
            "width": 98,
            "x": 572,
            "y": 848
        }

        self.assertEqual(expected_reply, lip_box_payload)


if __name__ == '__main__':
    unittest.main()
