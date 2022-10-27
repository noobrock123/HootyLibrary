import re
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def login_via_goolge(request):
    return render(request,'login_via_google/templates/hooty_library/index.html')