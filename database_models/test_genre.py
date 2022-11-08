from django.db import IntegrityError
from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
# Create your tests here.


class GenreTestCase(TestCase):
    def setUp(self) -> None:
        self.genre1 = Genre.objects.create(
            genre_list='genre1'
        )

    def test_genre_create_correct(self):
        self.assertEqual(self.genre1.genre_list, 'genre1')

    def test_genre_list_is_unique(self):
        with self.assertRaises(Exception) as raised:
            Genre.objects.create(
                genre_list='genre1'
            )
        self.assertEqual(IntegrityError, type(raised.exception))
