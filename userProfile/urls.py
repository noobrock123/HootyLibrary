from django.urls import include, path
from . import views

app_name = "userProfile"
urlpatterns = [
    path('user_profile/edit_profile/<str:user_id>', views.editProfile, name='editProfile'),
    path('user_profile/<str:user_id>', views.userProfile, name='userProfile'),
    path('user_profile/user_picture/<str:user_id>', views.user_picture, name='user_picture'),

]