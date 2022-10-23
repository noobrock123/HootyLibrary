from django.urls import include, path
from . import views
urlpatterns = [
    path('', view=views.home, name='home'),
    path('register/', view=views.register, name='register')

]