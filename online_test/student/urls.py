from django.urls import path
from . import views
urlpatterns = [
    path('fillDetails/',views.fillDetailView.as_view(),name='fillStudentDetail'),
    path('',views.QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:pk>/',views.take_quiz, name='take_quiz'),
    path('taken/', views.TakenQuizListView.as_view(), name='taken_quiz_list'),
    path('interests/', views.StudentInterestsView.as_view(), name='student_interests'),
    path('profile/<slug:slug>', views.student_detail_view.as_view(), name='student_profile'),
]