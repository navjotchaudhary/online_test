from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import redirect
from django.views import View
from accounts.models import User
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string


class loginView(View):
    def post(self,request):
        username        = request.POST.get('username')
        password        = request.POST.get('password')

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            if (user.is_student and user.has_details ==False):
                return redirect('fillStudentDetail')
            return redirect('home')
        else :
            context = {
                'message':'not able to login'
            }
            return render(request,'accounts/login.html',{'message':'not able to login'})
    
    
    def get(self,request):
        return render(request,'accounts/login.html',{'message':'try to login here'})



class logoutView(View):
    def get(self,request):
        auth.logout(request)
        return redirect('home')

class signupView(View):
    def post(self,request):
        username        = request.POST.get('username')
        password        = request.POST.get('password')
        confirm_password= request.POST.get('confirm_password')
        email           = request.POST.get('email')
        first_name      = request.POST.get('first_name')
        last_name       = request.POST.get('last_name')
        role            = request.POST.get('role')
        about            = request.POST.get('about')
        website            = request.POST.get('website')
        image = request.POST['imageselect']
        print(username,password,confirm_password,first_name,last_name,email)
        
        #user = User.objects.create_user(username = username, password = password,first_name = first_name, last_name = last_name,email=email)
        if password == confirm_password:
            if role == 'student':
                user = User.objects.create_user(is_active = False, is_student= True,username = username,about = about,image = "main_image/"+image, password = password,first_name = first_name, last_name = last_name,email=email)
                #put data into student table from here
            elif role == 'company':
                user = User.objects.create_user(is_active = False,is_company = True,username = username,website = website, about = about, image = "main_image/"+image, password = password,first_name = first_name, last_name = last_name,email=email)
                #put data into company table from 
            context = {
            'message':'user created sucessfully, check your email and activate your account',
            }
            site_name = get_current_site(request)
            domain = site_name.domain

            message = render_to_string("accounts/account_activate.html",{
            'domain': domain,
            'site_name': site_name,
            'token': account_activation_token.make_token(user),
            
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            })
        


            send_mail(
                'registered',
                f'you r {message}',
                'b.20.python.01.02@gmail.com',
                ['b.20.python.01.02@gmail.com'],
                fail_silently=False,
            )
        
            return render(request,'accounts/signup1.html',context)
        else:
            context = {
            'message':'password does not matched',
            }
            return render(request,'accounts/signup1.html',context)
    def get(self,request):
        context = {
            'message':'Signup here!',
        }
        return render(request,'accounts/signup1.html',context)

def activateAccount(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk = uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        
        return HttpResponse("<h3>You are activated now <a href ='../../../..'>visit Site..</a></h3>")
    else:
        print("Invalid Link")
        return HttpResponse("<h3>Invalid Link</h3>")