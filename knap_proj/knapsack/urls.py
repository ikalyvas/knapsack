from django.urls import path

from . import views

urlpatterns = [
    path('tasks', views.create_tasks, name='tasks'),
    path(r'tasks/<task_id>/', views.get_task, name='get_task'),
    path(r'solutions/<task_id>', views.get_solution, name='get_solution'),
    path(r'admin/tasks', views.get_all_tasks, name='get_all_tasks')

]