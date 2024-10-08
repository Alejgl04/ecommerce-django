from django.urls import path

from . import views

urlpatterns = [

  path('sign-up', views.sign_up, name='sign-up'),
  
  path('sign-in', views.sign_in, name='sign-in'),
  
  path('sign-out', views.sign_out, name='sign-out'),
  
  # Dashboard / profile 
 
  path('dashboard', views.dashboard, name='dashboard'),
  
  path('profile-management', views.profile_management, name='profile-management'),
  
  path('delete-account', views.delete_account, name='delete-account'),
  
  
  # Email verification Url's 
 
  path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
  
  path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
  
  path('email-verification-success', views.email_verification_success, name='email-verification-success'),
  
  path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),
  
  
  
]