from django.shortcuts import render
from database_models.models import Report

# Create your views here.

def show_admin_page(request):
    username = request.user.username
    reports = Report.objects.all()
    return render(request, 'admin_page/admin.html', {'admin_name':username,
    'reports': reports})