from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from exam.models import Quiz
from accounts.models import User

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
                    return render(request,'home/home1.html',{})
            else:
                return redirect('quizList')
        return render(request,'home/home1.html',context)
        

class aboutView(View):

    def get(self,request):
        
        return render(request,'home/about.html')
        