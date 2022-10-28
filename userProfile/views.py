from django.http import HttpResponse
from django.shortcuts import render
from database_models.models import *
# Create your views here.


def user_picture(request, user_id):
    try:
        with open(f'{User.objects.get(user_id=user_id).get_profile_pic()}', 'rb') as picture:
            return HttpResponse(picture.read(), content_type="image/jpeg")
    except:
        return HttpResponse('Not found')


def userProfile(request, user_id):
    user = User.objects.get(user_id=user_id)
    # if user == request.user:
    #     # in case user that access this profile is owner profile like user-1 access to user-1
    #     pass
    # else:
    #     # in case user that access this profile is other user
    #     pass
    context = {
        'my_books': Book.objects.filter(author=user.user_id),
        'bio': user.get_bio(),
        'username': user.get_username(),
        'gender': user.get_about_self()[0],
        'occupation': user.get_about_self()[2],
        'link': user.get_links(),
        'user': user,
        'user_picture': user_picture(request, user_id)

    }
    return render(request, 'userProfile/templates/userProfile/userProfile.html', context)
