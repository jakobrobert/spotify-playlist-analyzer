# WARNING Keep tests in root directory. Tried to move into "tests" directory,
# Got tests & dev working by using relative imports, but this broke uat / uwsgi. See #317

import unittest

from parameterized import parameterized

from core.analysis.super_genre_utils import SuperGenreUtils


class TestSuperGenre(unittest.TestCase):
    def test_empty_genres(self):
        genres = []
        expected_super_genres = [SuperGenreUtils.Others]
        actual_super_genres = SuperGenreUtils.get_super_genres_for_genres(genres)
        self.assertEqual(expected_super_genres, actual_super_genres)

    @parameterized.expand(["pop", "dance pop", "new romantic"])
    def test_Pop(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.Pop)

    @parameterized.expand(["rock", "hard rock", "mellow gold"])
    def test_Rock(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.Rock)

    @parameterized.expand(["edm", "dance", "house", "eurodance", "german dance"])
    def test_EDM(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.EDM)

    @parameterized.expand(["hip hop", "rap", "german rap"])
    def test_Rap(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.Rap)

    @parameterized.expand(["schlager", "discofox", "yodeling"])
    def test_Schlager(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.Schlager)

    @parameterized.expand(["black metal", "norwegian black metal", "death metal", "melodeath"])
    def test_ExtremeMetal(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.ExtremeMetal)

    @parameterized.expand(["metal", "symphonic metal", "funk metal", "neue deutsche harte", "industrial"])
    def test_Metal(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.Metal)

    @parameterized.expand(["classical", "opera", "french opera", "romanticism", "baroque"])
    def test_Classical(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.Classical)

    @parameterized.expand(["afrobeats", "r&b", "soul", "reggae", "jazz", "dancehall"])
    def test_Afro(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.Afro)

    @parameterized.expand(["unknown", "garbage", "foobar"])
    def test_Others(self, genre):
        self.__test_get_super_genre_for_genre(genre, SuperGenreUtils.Others)

    def test_multiple_genres_all_mapped(self):
        genres = ["pop", "dance pop", "eurodance", "dancehall", "black metal", "classical", "death metal"]
        expected_super_genres = [
            SuperGenreUtils.Pop, SuperGenreUtils.EDM, SuperGenreUtils.ExtremeMetal,
            SuperGenreUtils.Classical, SuperGenreUtils.Afro
        ]
        actual_super_genres = SuperGenreUtils.get_super_genres_for_genres(genres)
        self.assertEqual(expected_super_genres, actual_super_genres)

    def test_multiple_genres_all_not_mapped_then_super_genres_should_contain_only_Others(self):
        genres = ["unknown", "garbage", "foobar"]
        expected_super_genres = [SuperGenreUtils.Others]
        actual_super_genres = SuperGenreUtils.get_super_genres_for_genres(genres)
        self.assertEqual(expected_super_genres, actual_super_genres)

    def test_multiple_genres_some_not_mapped_then_super_genres_should_not_contain_Others(self):
        genres = ["unknown", "garbage", "foobar", "pop", "rock"]
        expected_super_genres = [SuperGenreUtils.Pop, SuperGenreUtils.Rock]
        actual_super_genres = SuperGenreUtils.get_super_genres_for_genres(genres)
        self.assertEqual(expected_super_genres, actual_super_genres)

    def __test_get_super_genre_for_genre(self, genre, expected_super_genre):
        actual = SuperGenreUtils.get_super_genre_for_genre(genre)
        self.assertEqual(expected_super_genre, actual)
