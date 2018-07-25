import unittest
from file import DiaryEntries

class TestDiaryEntries(unittest.TestCase):
    def setUp(self):
        self.my_diary = DiaryEntries()

    def test_entries(self):
        self.assertEqual(self.my_diary.Id, 1, msg='Error found')
        
    def test_post(self):
        self.my_diary.post(1)
        self.assertEqual(self.my_diary.Id, 2, msg='No post')

    def test_get_one(self):
        self.my_diary.get_one(1)
        self.assertEqual(self.my_diary.Id, 1, msg='Entry not found')

    def test_delete(self):
        self.my_diary.delete(1)
        self.assertEqual(self.my_diary.Id, 0, msg='Not deleted!')

    def test_get_all(self):
        self.my_diary.get_all(1)
        self.assertEqual(self.my_diary.Id, 1, msg='Entry not found')

    def test_put(self):
        self.my_diary.put(1)
        self.assertEqual(self.my_diary.Id, 1, msg='Update failed')