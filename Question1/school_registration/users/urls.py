from django.urls import path
from knox import views as knox_views

from .views import RegisterUser, Login

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='api-register'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('login/', Login.as_view(), name='login'),
]
