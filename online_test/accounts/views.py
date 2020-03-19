from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth

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
            return render(request,'accounts/login.html',context)
    
    else:
        return render(request,'accounts/login.html',{})