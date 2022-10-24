from django.urls import include, path
from . import views
urlpatterns = [
    path('userProfile/<str:username>', view=views.userProfile, name='userProfile')

]