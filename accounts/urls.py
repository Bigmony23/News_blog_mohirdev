
from django.urls import path, include
from .views import user_login
from django.contrib.auth import views
urlpatterns = [
    # path('login/',user_login, name='login'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]