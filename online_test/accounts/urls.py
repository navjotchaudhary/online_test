from django.urls import path
from . import views
##password reset
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/',views.loginView.as_view(),name = 'login'),
    path('logout/',views.logoutView.as_view(),name = 'logout'),
    path('signup/',views.signupView.as_view(),name = 'signup'),
    path('activate/<uidb64>/<token>/',views.activateAccount,name='activate'),
    ####################################################################
    #                       password reset                             #
    ####################################################################
    path('password-reset', auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset.html'), name='reset_password'),
    path('password-reset-done', auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_sent.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_complete.html'), name='password_reset_complete'),
        #~##########################################
]