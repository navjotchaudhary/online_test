from django.urls import path
from .views import quizDetail
urlpatterns = [
    path('detail/<int:pk>',quizDetail.as_view(),name = 'detail')
]