from django.urls import include, path
from . import views
urlpatterns = [
    path('userProfile/<str:user_id>', view=views.userProfile, name='userProfile'),
    path('userProfile/user_picture/<str:user_id>', views.user_picture, name='user_picture'),

]