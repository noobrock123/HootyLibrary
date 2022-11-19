from django.test import Client, TestCase
from database_models.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
# Create your tests here.


class BookFavoriteTestCase(TestCase):
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
        
        self.favorite1 = Favorite.objects.create(
            user_refer=self.user1,
            book_refer=self.book1,
        )
        
    def test_client_access_favorite_book_on_logged_in_favorited(self):
        # test client access favorited book on logged in
        # should redirect to book page and favorite was deleted 
        c = Client()
        c.login(username='user1', password='password')
        response = c.get(f'/book/{self.book1.book_id}/book_favorite/')
        with self.subTest():
            self.assertRedirects(response, f'/book/{self.book1.book_id}/', status_code=302,
                                 target_status_code=200, fetch_redirect_response=True)
        with self.subTest():
            favorite = Favorite.objects.filter(book_refer=self.book1, user_refer=self.user1).exists()
            self.assertFalse(favorite)
    def test_client_access_favorite_book_on_logged_in_not_favorite(self):
        # test client access not favorite book on logged in
        # should redirect to login page and favorite was created 
        c = Client()
        c.login(username='user1', password='password')
        response = c.get(f'/book/{self.book2.book_id}/book_favorite/')
        with self.subTest():
            self.assertRedirects(response, f'/book/{self.book2.book_id}/', status_code=302,
                                 target_status_code=200, fetch_redirect_response=True)
        with self.subTest():
            favorite = Favorite.objects.filter(book_refer=self.book2, user_refer=self.user1).exists()
            self.assertTrue(favorite)
    def test_client_access_favorite_book_on_not_logged_in(self):
        # test client access favorite book on not logged in 
        c = Client()
        response = c.get(f'/book/{self.book1.book_id}/book_favorite/')
        self.assertRedirects(response, f'/registeration/sign_in/?next=/book/{self.book1.book_id}/book_favorite/', status_code=302,
            target_status_code=200, fetch_redirect_response=True)