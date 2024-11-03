from django.urls import path
from . import views

urlpatterns = [
   path('register/',views.UserRegistrationView.as_view(),name='register'),
   path('login/',views.UserLoginView.as_view(),name='login'),
   path('users/',views.UserListView.as_view(),name='user_list'),
   path('users/<int:user_id>/',views.UserDetailView.as_view(),name='user_detail'),
   path('task/',views.TaskListView.as_view(),name = 'task_list'),
   path('task/<int:task_id>/',views.TaskDetailView.as_view(),name = 'task_detail'),
]