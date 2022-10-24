from django import views
from django.shortcuts import render
from database_models.models import *
# Create your views here.
def userProfile(request, username):
    user = User.objects.get(username=username)
    # if user == request.user:
    #     # in case user that access this profile is owner profile like user-1 access to user-1
    #     pass
    # else:
    #     # in case user that access this profile is other user
    #     pass
    context = {
        'my_books': Book.objects.filter(author=user.user_id),
        'bio': user.get_bio(),
        'username':user.get_username(),
        'gender':user.get_about_self()[0],
        'occupation':user.get_about_self()[2],
        'link':user.get_links(),
        'user':user,

    }
    return render(request, 'userProfile.html', context)