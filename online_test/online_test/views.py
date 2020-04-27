from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

class homeView(View):

    def get(self,request):
        if(request.user.is_authenticated):
            if(request.user.is_student):
                if(request.user.has_details == False):
                    return redirect('fillStudentDetail')
                else:
                    return render(request,'home/home.html',{})
            else:
                return redirect('quizList')
        return render(request,'base.html',{})
        