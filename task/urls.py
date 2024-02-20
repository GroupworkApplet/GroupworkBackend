from django.urls import path
from .views import (
    CreateTaskView,
    TaskDetailsView,
    TaskProgressDetailsView,
    TaskAssignmentList,
    TaskAssignmentDetail
)

urlpatterns = [
    # 任务创建
    path('tasks/', CreateTaskView.as_view(), name='create-task'),
    # 任务详情（获取、更新、删除）
    path('tasks/<int:pk>/', TaskDetailsView.as_view(), name='task-details'),
    # 任务进度详情（获取、更新）
    path('task-progress/<int:pk>/', TaskProgressDetailsView.as_view(), name='task-progress-details'),
    # 任务分配列表（获取、创建）
    path('task-assignments/', TaskAssignmentList.as_view(), name='task-assignments-list'),
    # 任务分配详情（获取、更新、删除）
    path('task-assignments/<int:pk>/', TaskAssignmentDetail.as_view(), name='task-assignment-detail'),
]

