from django.shortcuts import render
from django.views.generic import DetailView
from .models import Quiz
from student.models import TakenQuiz
# Create your views here.


class quizDetail(DetailView):
    template_name = 'exam/detail.html'
    model = Quiz
    context_object_name = 'quiz'
    def get_context_data(self,**kwargs):
            print(self.get_object())
            context = super(quizDetail,self).get_context_data(**kwargs)
            context['student']= self.request.user.student
            context['taken_Quiz'] = self.quizinlist(TakenQuiz.objects.filter(student = context['student']))
            return context
    def quizinlist(self,qlist):
        for quiz1 in qlist:
            print(quiz1.quiz)
            if self.get_object()==quiz1.quiz:
                return True
            
        return False

