from django.urls import path
from . import views

urlpatterns = [
   path('register/',views.UserRegistrationView.as_view(),name='register'),
   path('login/',views.UserLoginView.as_view(),name='login'),
   path('users/',views.UserListView.as_view(),name='user_list'),
]