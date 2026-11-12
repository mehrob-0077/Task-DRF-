from django.urls import path
from .views import (category_list_view, category_create_view, category_detail_view, category_update_view, category_delete_view,task_list_view, task_create_view, task_detail_view, task_update_view, task_delete_view)

urlpatterns = [
    path('', category_list_view, name='category-list-create'),   
    path('categories/create/', category_create_view, name='category-create'),
    path('categories/<int:id>/', category_detail_view, name='category-detail'), 
    path('categories/update/<int:id>/', category_update_view, name='category-update'),
    path('categories/delete/<int:id>/', category_delete_view, name='category-delete'),
    path('tasks/', task_list_view, name='task-list-create'),
    path('tasks/create/', task_create_view, name='task-create'),
    path('tasks/<int:id>/', task_detail_view, name='task-detail'),
    path('tasks/update/<int:id>/', task_update_view, name='task-update'),
    path('tasks/delete/<int:id>/', task_delete_view, name='task-delete'),
]