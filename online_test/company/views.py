from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.views import View
from django.views.generic import UpdateView,ListView, DetailView
from exam.forms import QuizCreationForm,QuestionForm,BaseAnswerInlineFormSet
from django.http import HttpResponse
from exam.models import Quiz,Question, Answer
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.db import transaction
# Create your views here.
class CreateQuiz(View):
    def get(self,request):
        context ={
            'form':QuizCreationForm,
        }
        
        return render(request,'company/createQuiz.html',context)
    def  post(self,request):
        owner = request.user
        form = QuizCreationForm(request.POST or None)
        
        print(form.is_valid())
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect("updateQuiz",post.pk)
        else:
            redirect("updateQuiz",post.pk)
            print(form.errors)
        redirect("updateQuiz",post.pk)

class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'subject', )
    context_object_name = 'quiz'
    template_name = 'company/QuizUpdate.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('updateQuiz', kwargs={'pk': self.object.pk})


class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'company/QuizList.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('subject') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset




def question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            #messages.success(request, 'You may now add answers/options to the question.')
            return redirect('changeQuestion', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'company/addQuestion.html', {'quiz': quiz, 'form': form})



def question_change(request, quiz_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            #messages.success(request, 'Question and answers saved with success!')
            return redirect('updateQuiz', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    return render(request, 'company/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })

class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'company/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

    