import unittest
from las import LASReader

class LasTests(unittest.TestCase):
    def test_test(self):
         las = LASReader('las_input/Lasfiles/Penobscot_B-41_LASOut_W4.las')
         self.assertEqual(las.curves.names[0],'DEPTH')
         self.assertEqual(las.curves.names[3],'DEPTH1')
