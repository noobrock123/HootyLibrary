from django.urls import include, path
from . import views

#from django.contrib import admin
#from django.conf import settings
#from django.conf.urls.static import static

app_name = "userProfile"
urlpatterns = [
    path('<str:user_id>/user_picture/',
         views.user_picture, name='user_picture'),
    path('edit_profile', views.editProfile, name='editProfile'),
    path('<str:user_id>', views.userProfile, name='user_profile'),

]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
