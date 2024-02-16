from django.urls import path
from .views import TaskDetails, TaskProgressDetails, TaskAssignmentList, TaskAssignmentDetail

urlpatterns = [
    path("TaskDetails/", TaskDetails),
    path("TaskProgressDetails/", TaskProgressDetails),
    path("TaskAssignmentList/", TaskAssignmentList),
    path("TaskAssignmentDetail/", TaskAssignmentDetail),
]