from django.urls import include, path
from . import views
app_name = "register"
urlpatterns = [
    path('', views.register, name='register'),

]
