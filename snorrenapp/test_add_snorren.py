import unittest
from add_snorren import Coordinate, FaceKeypoints, UpperLipBox


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mouth_left = Coordinate(1,1)
        mouth_right = Coordinate(1,1)
        nose = Coordinate(1,1)

        test_face = FaceKeypoints(mouth_left=mouth_left,
                                  mouth_right=mouth_right,
                                  nose=nose)

        test_lip_box = UpperLipBox(test_face)

        snorbox_payload = test_lip_box.response()

        self.assertEqual(Coordinate(2, 3), Coordinate(2, 3))
        self.assertEqual(snorbox_payload, Coordinate(2, 3))


if __name__ == '__main__':
    unittest.main()