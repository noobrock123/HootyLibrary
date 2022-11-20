from django.urls import include, path
from . import views

#from django.contrib import admin
#from django.conf import settings
#from django.conf.urls.static import static

app_name = "messaging"
urlpatterns = [
    path('<str:book_id>/reviews/', views.reviews, name='reviews'),
    path('<str:book_id>/create_review/', views.create_review, name='create_review'),
    path('<str:book_id>/issues/', views.show_issues, name='issues'),
    path('<str:book_id>/issuing/', views.issuing, name='issuing'),

]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
