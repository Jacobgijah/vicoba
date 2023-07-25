from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
import json
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
from django.contrib import auth


# views here.
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        
        # check if it contains alphanumeric charater
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
        return JsonResponse({'username_valid': True})
        # check if username has already taken or exists on database
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error':'sorry username in use, choose another one'}, status=409)
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        
        # check if it contains alphanumeric charater
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400)
        return JsonResponse({'username_valid': True})
        # check if username has already taken or exists on database
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error':'sorry email in use, choose another one'}, status=409)
        return JsonResponse({'email_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        #GET USER DATA   
        #VALIDATE
        #create a user account
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context  = {
            'fieldValues': request.POST
        }
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                
                if len(password) < 8:
                    messages.error(request, 'Password should contain atleast 8 characters')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                # path to view
                    # - getting domain we are on
                    # - getting relative url to verification
                    # - encode uid
                    # - token the user is going to use to verify (used once)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                                            'uidb64':uidb64, 'token':account_activation_token.make_token(user)})
                
                activate_url = 'http://'+domain+link
                
                email_subject = 'Activate your email'
                
                email_body = 'Hello '+user.username+', Please use this link to verify your account\n'+activate_url
                                
                recipient_email = email
                
                email = EmailMessage (
                    email_subject,
                    email_body, 'noreply@me.com',
                    to=[recipient_email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account created succcessfully')
                return render(request, 'authentication/register.html')
                
        messages.error(request, 'Sorry! Username or Email already taken')       
        return render(request, 'authentication/register.html', context)
    

class VerificationView(View):
    def get(self, request, uidb64, token):
        
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            
            messages.success(request, 'Account activated successfully')
            return redirect('login')
        
        except Exception as e:
            pass    
        
        messages.warning(request, 'Account already activated')
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome, "+user.username+" you are now logged in")
                    return redirect('dashboard')
                messages.error(request, "Account is not active, please check your email")
                return render(request, 'authentication/login.html')
        
            messages.error(request, "Invalid credentials, Try again")
            return render(request, 'authentication/login.html')
        
        messages.error(request, "Username or Password empty, Please fill all fields.")
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')