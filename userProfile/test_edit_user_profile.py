from django.test import TestCase
from database_models.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.contrib.messages import get_messages
# Create your tests here.


class EditUserProfielTestCase(TestCase):
    def setUp(self) -> None:
        with open('userProfile/test_media/owl.jpg', 'rb') as profile_pic:
            self.user1 = User.objects.create_user(
                username='user1',
                alias_name='user1_alias_name',
                email='user1@email.email',
                password='password',
                gender="Garfiw'sGender",
                age=16,
                occupation='user1 occupation',
                bio='user bio',
                social_link='www.user1_social_link.user1',
                donation_link='www.user1_donation_link.user1',
                profile_pic=SimpleUploadedFile(
                    name='owl.jpg', content=profile_pic.read(), content_type='image/jpeg'),
            )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@email.email',
            password='password'
        )

    def test_client_can_access_edit_user_profile_on_logged_in(self):
        # test client access to edit user profile when client was logged in
        c = Client()
        c.login(username='user1', password='password')
        response = c.get(f'/user_profile/edit_profile/')
        self.assertEqual(response.status_code, 200)

    def test_client_redirect_to_login_page_edit_user_profile_on_not_logged_in(self):
        # test client access to edit user profile when client was not logged in and should redirect to login page
        c = Client()
        response = c.get(f'/user_profile/edit_profile/')
        self.assertRedirects(response, f'/registeration/sign_in/?next=/user_profile/edit_profile/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_client_can_get_correct_user_profile_info(self):
        # test client get correct user profile info
        c = Client()
        c.login(username='user1', password='password')
        response = c.get(f'/user_profile/edit_profile/')
        self.assertEqual(response.context['user'], self.user1)

    def test_client_edit_correct_user_profile(self):
        # test client edit correct user profile and should redirect to their user profile page
        c = Client()
        c.login(username='user1', password='password')
        with open('userProfile/test_media/unknown.png', 'rb') as picture_profile:
            post = {
                'alias_name': 'user1 alias_name edited',
                'email': 'user1_edited@email.email',
                'gender': 'u1GenderEdited',
                'age': 15,
                'occupation': 'user1 occupation edited',
                'bio': 'user1 bio edited',
                'social_link': 'user1 social link edited',
                'donation_link': 'user1 donation link edited',
                'profile_pic': SimpleUploadedFile(
                    name='unknown.jpg', content=picture_profile.read(), content_type='image/jpeg'),
            }
        response = c.post(f'/user_profile/edit_profile/',
                          data=post, format='text/html')
        self.user1.refresh_from_db()

        messages = list(get_messages(response.wsgi_request))
        with self.subTest():
            self.assertRedirects(response, f'/user_profile/{self.user1.user_id}/', status_code=302,
                                 target_status_code=200, fetch_redirect_response=True)
        with self.subTest():
            self.assertEqual(
                str(messages[0]), 'Successful,Your profile has been edited.')
        with self.subTest():
            self.assertEqual(self.user1.alias_name, 'user1 alias_name edited')
        with self.subTest():
            self.assertEqual(self.user1.email, 'user1_edited@email.email')
        with self.subTest():
            self.assertEqual(self.user1.gender, 'u1GenderEdited')
        with self.subTest():
            self.assertEqual(self.user1.age, 15)
        with self.subTest():
            self.assertEqual(self.user1.occupation, 'user1 occupation edited')
        with self.subTest():
            self.assertEqual(self.user1.bio, 'user1 bio edited')
        with self.subTest():
            self.assertEqual(self.user1.social_link,
                             'user1 social link edited')
        with self.subTest():
            self.assertEqual(self.user1.donation_link,
                             'user1 donation link edited')

        with self.subTest():
            with open(f'{self.user1.profile_pic.path}', 'rb') as edited_picture_profile, open('userProfile/test_media/unknown.png', 'rb') as picture_profile:
                self.assertEqual(edited_picture_profile.read(),
                                 picture_profile.read())

    def test_client_edit_invalid_email_form(self):
        # test client post email with invalid email form
        c = Client()
        c.login(username='user1', password='password')

        with open('userProfile/test_media/unknown.png', 'rb') as picture_profile:
            post = {
                'alias_name': 'user1 alias_name edited',
                'email': 'user1_edited',
                'gender': 'u1GenderEdited',
                'age': 15,
                'occupation': 'user1 occupation edited',
                'bio': 'user1 bio edited',
                'social_link': 'user1 social link edited',
                'donation_link': 'user1 donation link edited',
                'profile_pic': SimpleUploadedFile(
                    name='unknown.jpg', content=picture_profile.read(), content_type='image/jpeg'),
            }
        response = c.post(f'/user_profile/edit_profile/',
                          data=post, format='text/html')
        messages = list(get_messages(response.wsgi_request))

        self.user1.refresh_from_db()
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertEqual(str(messages[0]), 'Enter a valid email address.')
        with self.subTest():
            self.assertEqual(self.user1.alias_name, 'user1_alias_name')
        with self.subTest():
            self.assertEqual(self.user1.email, 'user1@email.email')

        with self.subTest():
            self.assertEqual(self.user1.gender, "Garfiw'sGender")
        with self.subTest():
            self.assertEqual(self.user1.age, 16)
        with self.subTest():
            self.assertEqual(self.user1.occupation, 'user1 occupation')
        with self.subTest():
            self.assertEqual(self.user1.bio, 'user bio')
        with self.subTest():
            self.assertEqual(self.user1.social_link,
                             'www.user1_social_link.user1')
        with self.subTest():
            self.assertEqual(self.user1.donation_link,
                             'www.user1_donation_link.user1')
        with self.subTest(), open(self.user1.profile_pic.path, 'rb') as profile_pic, open('userProfile/test_media/owl.jpg', 'rb') as pic:
            self.assertEqual(profile_pic.read(), pic.read())

    def test_client_edit_used_email(self):
        # test client post email with used email
        c = Client()
        c.login(username='user1', password='password')
        with open('userProfile/test_media/unknown.png', 'rb') as picture_profile:
            post = {
                'alias_name': 'user1 alias_name edited',
                'email': 'user2@email.email',
                'gender': 'u1GenderEdited',
                'age': 15,
                'occupation': 'user1 occupation edited',
                'bio': 'user1 bio edited',
                'social_link': 'user1 social link edited',
                'donation_link': 'user1 donation link edited',
                'profile_pic': SimpleUploadedFile(
                    name='unknown.jpg', content=picture_profile.read(), content_type='image/jpeg'),
            }
        response = c.post(f'/user_profile/edit_profile/',
                          data=post, format='text/html')
        messages = list(get_messages(response.wsgi_request))
        self.user1.refresh_from_db()
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertEqual(
                str(messages[0]), 'User with this Email already exists.')
        with self.subTest():
            self.assertEqual(self.user1.alias_name, 'user1_alias_name')
        with self.subTest():
            self.assertEqual(self.user1.email, 'user1@email.email')

        with self.subTest():
            self.assertEqual(self.user1.gender, "Garfiw'sGender")
        with self.subTest():
            self.assertEqual(self.user1.age, 16)
        with self.subTest():
            self.assertEqual(self.user1.occupation, 'user1 occupation')
        with self.subTest():
            self.assertEqual(self.user1.bio, 'user bio')
        with self.subTest():
            self.assertEqual(self.user1.social_link,
                             'www.user1_social_link.user1')
        with self.subTest():
            self.assertEqual(self.user1.donation_link,
                             'www.user1_donation_link.user1')
        with self.subTest(), open(self.user1.profile_pic.path, 'rb') as profile_pic, open('userProfile/test_media/owl.jpg', 'rb') as pic:
            self.assertEqual(profile_pic.read(), pic.read())
