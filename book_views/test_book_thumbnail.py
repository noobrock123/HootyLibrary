from django.test import Client, TestCase
from database_models.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
# Create your tests here.


class ThumbnailTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='user1',
            password='password',
            email='user1@email.email'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password',
            email='user2@email.email'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            password='password',
            email='user3@email.email'
        )
        self.genre1 = Genre.objects.create(
            genre_list='genre1'
        )
        self.genre2 = Genre.objects.create(
            genre_list='genre2'
        )
        self.book1 = Book.objects.create(
            book_name='book1',
            author=self.user1,
            book_type=1,
            genres=('genre1', )
        )
        self.book2 = Book.objects.create(
            book_name='book2',
            author=self.user2,
            book_type=2,
            genres=('genre1', 'genre2')
        )
        self.book3 = Book.objects.create(
            book_name='book3',
            author=self.user2,
            book_type=1,
            genres=('genre1', 'genre2'),
            description='This is book3 description',
            thumbnail=SimpleUploadedFile(name='RH_StudyGuide.jpg', content=open(
                'book_views/test_data/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='image/jpeg'),
            pdf_files=SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'book_views/test_data/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf'),
        )
        
    def test_client_can_access_book_thumbnail_set(self):
        # test client can access book's thumbnail not set
        c = Client()
        response = c.get(f'/book/{self.book3.book_id}/thumbnail/')
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            with open('book_views/test_data/RH_StudyGuide_V2.pdf', 'rb') as thumbnail:
                self.assertEqual(thumbnail.read(), response.content)

    def test_client_can_access_book_thumbnail_not_set(self):
        # test client can access book's thumbnail not set
        c = Client()
        response = c.get(f'/book/{self.book1.book_id}/thumbnail/')
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            with open(f'book_views/static/bookpage/images/not found book.jpg', 'rb') as no_thumbnail:
                self.assertEqual(no_thumbnail.read(), response.content)
