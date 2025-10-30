
from django.urls import path, include
from .views import user_login, dashboard_view, user_register, SignupView
from django.contrib.auth import views
urlpatterns = [
    # path('login/',user_login, name='login'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),

    path('password_reset/',
         views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html'
         ),
         name='password_reset'),

    path('password_reset/done/',
         views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('profile/', dashboard_view, name='user_profile'),
    # path('signup/', user_register, name='user_register'),
    path('signup/', SignupView.as_view(),name='signin'),
]