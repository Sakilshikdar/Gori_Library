
from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.UserRegistationView.as_view(), name='register'),
    path('login/', views.UserLogintView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserBankAccountUpdateView.as_view(), name='profile'),
]
