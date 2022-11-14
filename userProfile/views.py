from django.http import HttpResponse
from django.shortcuts import redirect, render
from database_models.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def user_picture(request, user_id):
    try:
        with open(f'{User.objects.get(user_id=user_id).profile_pic.path}', 'rb') as picture:
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
        'my_books': Book.objects.filter(author=user),
        'bio': user.get_bio(),
        'username': user.get_username(),
        'gender': user.get_about_self()[0],
        'occupation': user.get_about_self()[2],
        'link': user.get_links(),
        'user': user,
        'user_picture': user_picture(request, user_id)

    }
    return render(request, 'userProfile/userProfile.html', context)


@login_required()
def editProfile(request, user_id):

    try:
        user = User.objects.get(user_id=user_id)
    except:
        return HttpResponse('Not Found')
    if request.user != user:
        return HttpResponse('You are not allowed to edit this user')
    else:
        context = {
            'user': user,
        }
        if request.method == 'POST':
            cancel = request.POST.get('cancel')
            if cancel:
                return redirect('MAIN_APP:home')
            alias_name = request.POST.get('alias_name')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            occupation = request.POST.get('occupation')
            bio = request.POST.get('bio')
            social_link = request.POST.get('social_link')
            donation_link = request.POST.get('donation_link')
            profile_pic = request.POST.get('profile_pic')
            try:
                if user != User.objects.get(email=email):
                    messages.error('This email is already exist ! ! !')
                    return render(request, 'editProfile/editProfile.html', context)
            except:
                pass
            user.alias_name = alias_name
            user.email = email if email != '' else user.email
            user.gender = gender
            if not age:
                print(age)
                user.age = None
            else:
                user.age = age 
            user.occupation = occupation
            user.bio = bio
            user.social_link = social_link
            user.donation_link = donation_link
            user.profile_pic = profile_pic if profile_pic != None else user.profile_pic
            user.save()
            #return redirect('userProfile', user_id=user.user_id)
            return redirect('MAIN_APP:home')

    return render(request, 'editProfile/editProfile.html', context)
