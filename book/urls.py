
from django.urls import path
from .import views
urlpatterns = [
    path('', views.addPostCreateView.as_view(), name='home'),
    path('details/<int:id>/', views.PostDetailsView.as_view(), name='details_post'),
    # path('details/<int:id>/', views.buy_car, name='details_post'),
]
