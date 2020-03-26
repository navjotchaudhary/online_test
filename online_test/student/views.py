from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from .forms import StudentDetailsForm
from accounts.models import User
# Create your views here.
class fillDetailView(View):
    def get(self,request):
        context ={
            'form':StudentDetailsForm,
        }
        
        return render(request,'student/fillStudentsDetail.html',context)
    def post(self,request):
        user = request.user
        form = StudentDetailsForm(request.POST or None)
        
        print(form.is_valid())
        if form.is_valid():
            interests = form.cleaned_data['interests']
            AdharNumber = form.cleaned_data['AdharNumber']
            print("dgfsgfgh")
            print(interests,AdharNumber)
            post = form.save(commit=False)
            post.user = user
            post.save()
            User.objects.filter(pk=user.id).update(has_details=True)
        else:
            
            print(form.errors)