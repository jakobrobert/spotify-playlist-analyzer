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

    @parameterized.expand(["schlager"])
    def test_Schlager(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(SuperGenreUtils.Schlager, actual)

    # TODOLATER ExtremeMetal, Metal

    @parameterized.expand(["classical", "opera", "french opera"])
    def test_Classical(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(SuperGenreUtils.Classical, actual)

    @parameterized.expand(["classical", "opera", "french opera"])
    def test_Country(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(SuperGenreUtils.Classical, actual)

    @parameterized.expand(["afrobeats", "r&b", "soul"])
    def test_Afro(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(SuperGenreUtils.Afro, actual)

    @parameterized.expand(["unknown", "garbage", "foobar"])
    def test_Others(self, genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(SuperGenreUtils.Others, actual)
