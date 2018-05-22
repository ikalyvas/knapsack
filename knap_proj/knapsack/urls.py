from django.urls import path,re_path

from . import views

urlpatterns = [
    path('tasks', views.create_tasks, name='tasks'),
    path(r'tasks/<task_id>/', views.get_task, name='get_task')

]