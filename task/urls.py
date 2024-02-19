from django.urls import path
from .views import TaskDetailsView, TaskProgressDetailsView, TaskAssignmentList, TaskAssignmentDetail

urlpatterns = [
    path('task/<int:pk>/', TaskDetailsView.as_view(), name='task-details'),
    path('task-progress/<int:pk>/', TaskProgressDetailsView.as_view(), name='task-progress-details'),
    path('task-assignments/', TaskAssignmentList.as_view(), name='task-assignment-list'),
    path('task-assignments/<int:pk>/', TaskAssignmentDetail.as_view(), name='task-assignment-detail'),
]
