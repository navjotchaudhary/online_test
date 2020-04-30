from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from exam.models import Quiz
from accounts.models import User, contactUs

class homeView(View):

    def get(self,request):
        Quizes = Quiz.objects.all()
        companies = User.objects.filter(is_company=True)
        context = {
            'Quizes':Quizes,
            'companies':companies
        }
        if(request.user.is_authenticated):
            if(request.user.is_student):
                if(request.user.has_details == False):
                    return redirect('fillStudentDetail')
                else:
                    return render(request,'home/home.html',context)
            else:
                return redirect('quizList')
        return render(request,'home/home.html',context)
        

class aboutView(View):

    def get(self,request):
        
        return render(request,'home/about.html')





class contactView(View):

    def get(self,request):
        
        return render(request,'home/contact.html')

    def post(self,request):
        name = request.POST.get('name')
        if request.user.is_authenticated:
            name = request.user.username
        email = request.POST.get('email')
        message = request.POST.get('message')
        a = contactUs.objects.create(name = name,email=email, message = message)
        a.save()
        context = {
            'message':name +", your message is saved successfully...."
        }
        return render(request,'home/contact.html',context)

          