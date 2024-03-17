from django.urls import path

from .views import (
    CreateTaskView,
    TaskDetailsView,
    TaskProgressDetailsView,
    TaskAssignmentList, TaskFound, getClockInfo,
)

urlpatterns = [
    # 任务创建
    path('tasks/', CreateTaskView.as_view(), name='create-task'),
    # 任务详情（获取、更新、删除）
    path('tasks/<int:pk>/', TaskDetailsView.as_view(), name='task-details'),
    # 任务进度详情（获取、更新）
    path('tasks/<int:pk>/task-progress/', TaskProgressDetailsView.as_view(), name='task-progress-details'),
    # 任务分配列表（获取、创建）
    path('tasks/<int:pk>/task-assignments/', TaskAssignmentList.as_view(), name='task-assignments-list'),
    # 任务分配详情（获取、更新、删除）
    path('tasks/<int:pk>/task-assignments/<int:assignment_id>/', TaskAssignmentList.as_view(), name='task-assignments-list'),
    path('task-find/<int:pk>/', TaskFound.as_view(), name='TaskFound'),
    # 获取打卡信息根据组
    path('getClockIn', getClockInfo.as_view(), name='get_clock_in/'),
]

