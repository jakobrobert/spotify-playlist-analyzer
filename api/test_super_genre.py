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
        self.assertEqual(SuperGenreUtils.Pop, actual)

    @parameterized.expand(["rock", "hard rock", "mellow gold"])
    def test_Rock(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(SuperGenreUtils.Rock, actual)

    @parameterized.expand(["edm", "dance", "house", "eurodance", "german dance"])
    def test_EDM(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(SuperGenreUtils.EDM, actual)

    @parameterized.expand(["hip hop", "rap", "german rap"])
    def test_Rap(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(SuperGenreUtils.HipHopOrRap, actual)
