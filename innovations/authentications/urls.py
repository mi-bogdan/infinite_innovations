from django.urls import path
from .views import LoginUser, logout_user, RegisterUser


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]
