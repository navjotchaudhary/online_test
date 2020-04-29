from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginView.as_view(),name = 'login'),
    path('logout/',views.logoutView.as_view(),name = 'logout'),
    path('signup/',views.signupView.as_view(),name = 'signup'),
    path('activate/<uidb64>/<token>/',views.activateAccount,name='activate'),
]