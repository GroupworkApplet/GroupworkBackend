from django.urls import path
from views import *

urlpatterns = [
    path('', GroupList.as_view()),
    path('<int:pk>/', GroupDetail.as_view()),
    path('<int:group_id>/members/', GroupMemberList.as_view()),
    path('<int:group_id>/members/<int:pk>/', GroupMemberDetail.as_view()),
    path('<int:group_id>/messages/', MessageList.as_view()),
    path('<int:group_id>/messages/<int:pk>/', MessageDetail.as_view()),
    path('<int:group_id>/documents/', DocumentList.as_view()),
    path('<int:group_id>/documents/<int:pk>/', DocumentDetail.as_view()),
    path('<int:group_id>/progress/', ProgressDetail.as_view()),

]