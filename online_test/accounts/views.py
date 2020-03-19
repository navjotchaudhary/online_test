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
            return HttpResponse(f'logged in as {user.username}')
        else :
            context = {
                'message':'not able to login'
            }
            return render(request,'accounts/login.html',{'message':'not able to login'})
    
    else:
        return render(request,'accounts/login.html',{})



def logout(request):
    auth.logout(request)
    return redirect('login')


def signup(request):
    if request.method=='POST':
        username        = request.POST.get('username')
        password        = request.POST.get('password')
        confirm_password= request.POST.get('password')
        email           = request.POST.get('email')
        first_name      = request.POST.get('first_name')
        last_name       = request.POST.get('last_name')
        role            = request.POST.get('role')
        print(username,password,confirm_password,first_name,last_name,email)
        #user = User.objects.create_user(username = username, password = password,first_name = first_name, last_name = last_name,email=email)
        if role == 'student':
            user = User.objects.create_user(is_student= True,username = username, password = password,first_name = first_name, last_name = last_name,email=email)
            #put data into student table from here
        elif role == 'company':
            user = User.objects.create_user(is_company = True,username = username, password = password,first_name = first_name, last_name = last_name,email=email)
            #put data into company table from here
    else:
        context = {
            'message':'hogya show',
        }
        return render(request,'accounts/signup.html',context)


