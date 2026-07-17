from django.urls import path
from tasks.views import add_task, delete_task, filter_tasks, home, login_view, update_task, register_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('add_task/', add_task, name='add_task'),
    path('tasks/<str:foo>/', filter_tasks, name='tasks'),
    path('task/<int:task_id>/', update_task, name='update_task'),
    path('task/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout')
    
]



