from django.urls import path
from . import views
urlpatterns =[
    path('quiz/create',views.CreateQuiz.as_view(),name='createQuiz'),
    path('quiz/<int:pk>',views.QuizUpdateView.as_view(),name= 'updateQuiz'),
    path('quiz/',views.QuizListView.as_view(),name='quizList'),
    path('quiz/<int:pk>/question/add',views.question_add,name='addQuestion'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>',views.question_change,name='changeQuestion')
]

