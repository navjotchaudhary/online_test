from django.urls import path
from . import views
urlpatterns = [
    path('fillDetails/',views.fillDetailView.as_view(),name='fillStudentDetail')
]