from django.urls import path
from .views import (GroupList, GroupDetail, GroupMemberList,
                    GroupMemberDetail, MessageList, MessageDetail,
                    DocumentList, DocumentDetail, ProgressDetail)

urlpatterns = [
    path('', GroupList.as_view()),
    path('<int:pk>/', GroupDetail.as_view(), name='group-detail'),
    path('<int:group_id>/members/', GroupMemberList.as_view(), name='group-member-list'),
    path('<int:group_id>/members/<int:pk>/', GroupMemberDetail.as_view(), name='group-member-detail'),
    path('<int:group_id>/messages/', MessageList.as_view(), name='message-list'),
    path('<int:group_id>/messages/<int:pk>/', MessageDetail.as_view(), name='message-detail'),
    path('<int:group_id>/documents/', DocumentList.as_view(), name='document-list'),
    path('<int:group_id>/documents/<int:pk>/', DocumentDetail.as_view(), name='document-detail'),
    path('<int:group_id>/progress/', ProgressDetail.as_view(), name='progress-detail'),

]