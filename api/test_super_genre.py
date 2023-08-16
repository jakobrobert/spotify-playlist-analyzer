import unittest

from core.analysis.super_genre_utils import SuperGenreUtils


class TestSuperGenre(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # TODONOW merge test_pop, maybe make parametrized test
    def test_pop_1(self):
        genre = "pop"
        expected = "Pop"

        actual = SuperGenreUtils.get_super_genre_for_genre(genre)

        self.assertEqual(expected, actual)

    def test_pop_2(self):
        genre = "dance pop"
        expected = "Pop"

        actual = SuperGenreUtils.get_super_genre_for_genre(genre)

        self.assertEqual(expected, actual)

    def test_pop_3(self):
        genre = "new romantic"
        expected = "Pop"

        actual = SuperGenreUtils.get_super_genre_for_genre(genre)

        self.assertEqual(expected, actual)

    def test_edm(self):
        genre = "hip house"
        expected = "EDM"

        actual = SuperGenreUtils.get_super_genre_for_genre(genre)

        self.assertEqual(expected, actual)
