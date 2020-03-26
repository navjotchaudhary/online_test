from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import redirect
from django.views import View
from accounts.models import User



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
            if role == 'student':
                return redirect('fillStudentDetail')
            else:
                return render(request,'accounts/signup.html',context)
        else:
            context = {
            'message':'password does not matched',
            }
            return render(request,'accounts/signup.html',context)
    def get(self,request):
        context = {
            'message':'Signup here!',
        }
        return render(request,'accounts/signup.html',context)

        