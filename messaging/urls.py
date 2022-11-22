from django.urls import include, path
from . import views

#from django.contrib import admin
#from django.conf import settings
#from django.conf.urls.static import static

app_name = "messaging"
urlpatterns = [
    path('reviews/', views.reviews, name='reviews'),
    path('create_review/', views.create_review, name='create_review'),
    path('issues/', views.show_issues, name='issues'),
    path('create_issue/', views.create_issue, name='create_issue'),
    path('create_report/', views.create_report, name='create_report'),

]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
