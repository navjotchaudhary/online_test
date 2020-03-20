from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import redirect

from accounts.models import User



# Create your views here.
def login(request):
    if request.method=='POST':
        username        = request.POST.get('username')
        password        = request.POST.get('password')

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else :
            context = {
                'message':'not able to login'
            }
            return render(request,'accounts/login.html',{'message':'not able to login'})
    
    else:
        return render(request,'accounts/login.html',{'message':'try to login here'})



def logout(request):
    auth.logout(request)
    return redirect('home')


def signup(request):
    if request.method=='POST':
        username        = request.POST.get('username')
        password        = request.POST.get('password')
        confirm_password= request.POST.get('confirm_password')
        email           = request.POST.get('email')
        first_name      = request.POST.get('first_name')
        last_name       = request.POST.get('last_name')
        role            = request.POST.get('role')
        print(username,password,confirm_password,first_name,last_name,email)
        
        #user = User.objects.create_user(username = username, password = password,first_name = first_name, last_name = last_name,email=email)
        if password == confirm_password:
            if role == 'student':
                user = User.objects.create_user(is_student= True,username = username, password = password,first_name = first_name, last_name = last_name,email=email)
                #put data into student table from here
            elif role == 'company':
                user = User.objects.create_user(is_company = True,username = username, password = password,first_name = first_name, last_name = last_name,email=email)
                #put data into company table from 
            context = {
            'message':'user created sucessfully',
            }
            return render(request,'accounts/signup.html',context)
        else:
            context = {
            'message':'password does not matched',
            }
            return render(request,'accounts/signup.html',context)

    else:
        context = {
            'message':'Signup here!',
        }
        return render(request,'accounts/signup.html',context)


