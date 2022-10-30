from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views as views

urlpatterns = [
    # path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="login_logout/password_reset.html"), 
         name="reset_password"),

    path('reset_password_sent/', 
         auth_views.PasswordChangeDoneView.as_view(template_name="login_logout/password_reset_sent.html"), 
         name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="login_logout/password_reset_form.html"), 
         name="password_reset_confirm"),
    
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="login_logout/password_reset_done.html"), 
         name="password_reset_complete"),
]

# 1 - Submit email form                      // PasswordResetView.as_view()
# 2 - Email sent success messege             // PasswordChangeDoneView.as_view()
# 3 - Link to password reset form in email   // PasswordResetConfirmView.as_view()
# 4 - Password successfully changed message  // PasswordResetCompleteView.as_view()