from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.register, name='register'),
<<<<<<< HEAD
=======
    #path('register/', views.register, name='register')
>>>>>>> 6071948 (Linking homepage and make static files)

]