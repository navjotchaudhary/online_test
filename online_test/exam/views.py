from django.shortcuts import render
from django.views.generic import DetailView
from .models import Quiz
# Create your views here.


class quizDetail(DetailView):
    template_name = 'exam/detail.html'
    model = Quiz
    context_object_name = 'quiz'
    

