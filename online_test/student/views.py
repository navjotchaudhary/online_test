from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from .forms import StudentDetailsForm, TakeQuizForm, StudentInterestsForm
from accounts.models import User
from django.views.generic import ListView, UpdateView, DetailView
from exam.models import Quiz
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import TakenQuiz
from django.contrib import messages
from .models import Student
from django.urls import reverse_lazy
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


class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'student/quiz_list.html'

    def get_queryset(self):
        student = self.request.user
        student = Student.objects.get(user=student)
        print(f'student {student}')
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'student/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })


class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'student/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset

class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'student/interests_form.html'
    success_url = reverse_lazy('quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)




class student_detail_view(DetailView):
    model = User
    template_name = "student/profile.html"
    def get_context_data(self,**kwargs):
            print(self.get_object())
            context = super(student_detail_view,self).get_context_data(**kwargs)
            context['student']= Student.objects.get(user = self.get_object())
            context['taken_Quiz'] = TakenQuiz.objects.filter(student = context['student'])
            return context

