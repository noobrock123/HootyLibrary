from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.register, name='register'),
    #path('register/', views.register, name='register')

]