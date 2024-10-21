from django.urls import path
from tasks.views import CreateUserView, TaskCreateView, AssignTaskView, UserTasksView, home, user_list, task_list

urlpatterns = [
    path('tasks/', task_list, name='task-list'),  # URL for getting list of tasks
    path('users/', user_list, name='user-list'),
    path('', home, name='home'),  # Set home page route
    path('users/create/', CreateUserView.as_view(), name='user-create'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:task_id>/assign/', AssignTaskView.as_view(), name='task-assign'),
    path('users/<int:user_id>/tasks/', UserTasksView.as_view(), name='user-tasks'),
]
