from django.test import TestCase
from database_models.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
# Create your tests here.

class userProfileTestCase(TestCase):
    def setUp(self):
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
                profile_pic=SimpleUploadedFile(name='RH_StudyGuide.jpg', content=profile_pic.read(), content_type='image/jpeg'),
            )
        self.user2 = User.objects.create_user(
                username='user2',
                alias_name='user2_alias_name',
                email='user2@email.email', 
                password='password',
                gender="Garfiw'sGender",
                age=16,
                occupation='user2 occupation',
                bio='user bio',
                social_link='www.user2_social_link.user2',
                donation_link='www.user2_donation_link.user2',
                # profile_pic=SimpleUploadedFile(name='RH_StudyGuide.jpg', content=profile_pic.read(), content_type='image/jpeg'),
            )
    def test_client_can_access_user_picture(self):
        c = Client()
        response = c.post(f'/userProfile/user_picture/{self.user1.user_id}')
        self.assertEqual(response.status_code, 200)
    def test_client_access_user_picture_does_not_set(self):
        c = Client()
        response = c.post(f'/userProfile/user_picture/{self.user2.user_id}')
        self.assertEqual(response.status_code, 200)
    def test_client_recieve_correct_user_picture(self):
        c = Client()
        response = c.post(f'/userProfile/user_picture/{self.user1.user_id}')
        with open(self.user1.profile_pic.path,'rb') as profile_pic:
            self.assertEqual(response._container[0], profile_pic.read())
    def test_client_can_access_user_profile(self):
        c = Client()
        response = c.post(f'/userProfile/{self.user1.user_id}')
        self.assertEqual(response.status_code, 200)
    # def test_client_recieve_correct_user_profile(self):
    #     c = Client()
    #     response = c.post(f'userProfile/{self.user1.user_id}')
    #     print(response.__dict__)