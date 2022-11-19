from django.test import Client, TestCase
from database_models.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
# Create your tests here.


class BookViewTestCase(TestCase):
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
        
    
    def test_client_access_book_does_not_exist(self):
        # test client access book does not exist
        c = Client()
        response = c.get(f'/book/waefawefwaef/')
        self.assertEqual(response.status_code,404)
    def test_client_access_book_no_logged_in(self):
        # test client access book when not logged in
        c = Client()
        response = c.get(f'/book/{self.book3.book_id}/')
        with self.subTest():
            self.assertEqual(response.context['book'], self.book3)
        with self.subTest():
            self.assertTemplateUsed(
                response, 'book_views/templates/book_views/index.html')

    def test_client_access_book_logged_in(self):
        # test client access book when logged in
        c = Client()
        c.login(username='user1', password='password')
        response = c.get(f'/book/{self.book3.book_id}/')
        self.book3.refresh_from_db()
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertEqual(response.context['book'], self.book3)
        with self.subTest():
            self.assertTemplateUsed(
                response, 'book_views/templates/book_views/index.html')
        with self.subTest():
            time_now = timezone.now()
            read = Read.objects.get(
                user_refer=self.user1, book_refer=self.book3)
            self.assertTrue(read.book_read_latest_time <=
                            time_now and read.book_read_latest_time + timedelta(seconds=1) >= time_now)
