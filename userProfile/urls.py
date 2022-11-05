from django.urls import include, path
from . import views
urlpatterns = [
    path('userProfile/editProfile/<str:user_id>', views.editProfile, name='editProfile'),
    path('userProfile/user_picture/<str:user_id>', views.user_picture, name='user_picture'),
    path('userProfile/<str:user_id>', view=views.userProfile, name='userProfile'),

]