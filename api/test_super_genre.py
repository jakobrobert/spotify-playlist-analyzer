import unittest

from parameterized import parameterized

from core.analysis.super_genre_utils import SuperGenreUtils


class TestSuperGenre(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @parameterized.expand(["pop", "dance pop", "new romantic"])
    def test_Pop(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual("Pop", actual)

    @parameterized.expand(["edm", "dance", "house", "eurodance", "german dance"])
    def test_EDM(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual("EDM", actual)
