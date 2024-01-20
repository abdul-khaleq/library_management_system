from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='user_signup'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('profile/', views.profile, name='profile'),
    path('', views.LogoutView.as_view(), name='user_logout'),
    path('deposit/', views.deposit, name='deposit'),
    path('return_book/<int:id>/', views.return_book, name='return_book'),
]