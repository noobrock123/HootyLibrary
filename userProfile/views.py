from django.http import HttpResponse
from django.shortcuts import redirect, render
from database_models.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sessions.models import Session

# Create your views here.


def user_picture(request, user_id):
    try:
        with open(f'{User.objects.get(user_id=user_id).profile_pic.path}', 'rb') as picture:
            return HttpResponse(picture.read(), content_type="image/jpeg")
    except:
        with open(f'userProfile/static/userProfile/images/default_user_profile.png', 'rb') as picture:
            return HttpResponse(picture.read(), content_type="image/jpeg")


def userProfile(request, user_id):
    user = User.objects.get(user_id=user_id)
    context = {
        'my_books': Book.objects.filter(author=user),
        'bio': user.bio,
        'username': user.username,
        'gender': user.gender,
        'occupation': user.occupation,
        'link': user.get_links(),
        'user_id': user.user_id,

    }
    return render(request, 'userProfile/userProfile.html', context)


@login_required(login_url='register:log_in')
def editProfile(request):
    user = request.user
    context = {
        'user': user,
    }
    if request.method == 'POST':
        alias_name = request.POST.get('alias_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        occupation = request.POST.get('occupation')
        bio = request.POST.get('bio')
        social_link = request.POST.get('social_link')
        donation_link = request.POST.get('donation_link')
        profile_pic = request.FILES.get('profile_pic')

        user.alias_name = alias_name
        user.email = email if email != '' else user.email
        user.gender = gender
        user.age = age
        user.occupation = occupation
        user.bio = bio
        user.social_link = social_link
        user.donation_link = donation_link
        user.profile_pic = profile_pic if profile_pic != None else user.profile_pic
        try:
            user.save()
        except Exception as exception:
            for e in exception:
                messages.error(request, e[1][0])
            return render(request, 'editProfile/editProfile.html', context)

        messages.success(request, 'Successful,Your profile has been edited.')
        return redirect('userProfile:user_profile', user_id=user.user_id)

    return render(request, 'editProfile/editProfile.html', context)
