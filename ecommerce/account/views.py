from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import User, auth

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .token import user_tokenizer_generate
from .forms import CreateUserForm, SignInForm, UpdateUserForm

# Create your views here.

def sign_up(request):
  
  form = CreateUserForm()
  
  if request.method == 'POST':
    
    form = CreateUserForm(request.POST)
    
    if form.is_valid():

      user = form.save()
      
      user.is_active = False
      
      user.save()
      
      # Email verification setup ( template )
      
      current_site = get_current_site(request)
      
      subject = 'Account verification email'
      
      message = render_to_string('account/registration/email-verification.html', {
        
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': user_tokenizer_generate.make_token(user),

      })
      
      user.email_user(subject=subject, message=message)
      
      return redirect('email-verification-sent')

  
  context = { 'form': form }
   
  return render(request, 'account/registration/sign-up.html', context)


def email_verification(request, uidb64, token):
  
  user_id = force_str(urlsafe_base64_decode(uidb64))
  
  user = User.objects.get(pk=user_id)

  if user and user_tokenizer_generate.check_token(user, token):
    
    user.is_active = True   

    user.save()
    
    return redirect('email-verification-success')
  
  else:
    
    return redirect('email-verification-failed')


def email_verification_sent(request):
  
  return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
  
  return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
  
  return render(request, 'account/registration/email-verification-failed.html')


def sign_in(request):
  
  form = SignInForm()
  
  if request.method == 'POST':
    
    form = SignInForm(request, data=request.POST)
    
    if form.is_valid():
      
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username=username, password=password)
      
      if user is not None:
        auth.login( request, user )
        return redirect('dashboard')
  
  context = { 'form': form }
  return render(request, 'account/sign-in.html', context=context)


def sign_out(request):
  
  auth.logout(request)
  
  return redirect('store')
  

@login_required(login_url='sign-in')
def dashboard(request):
  return render(request, 'account/dashboard.html')


@login_required(login_url='sign-in')
def profile_management(request):
  
  #Update email and username  
  user_form = UpdateUserForm(instance=request.user)
  
  if request.method == 'POST':
    user_form = UpdateUserForm(request.POST, instance=request.user)
    
    if user_form.is_valid():
      
      user_form.save()
  
      return redirect('dashboard')
    
  context = {'user_form': user_form}
  
  return render(request, 'account/profile-management.html', context)


@login_required(login_url='sign-in')
def delete_account(request):
  
  user = User.objects.get(id=request.user.id)
  
  if request.method == 'POST':
    
    user.delete()
    
    return redirect('store')
    
  return render(request, 'account/delete-account.html')
