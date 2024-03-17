from django.urls import path

from .views import (GroupList, GroupDetail, GroupMemberList, UploadFile,
                    GroupMemberDetail, MessageList, MessageDetail,
                    DocumentList, DocumentDetail, ProgressDetail, getid, groupLeader, groupget, GetImage)

urlpatterns = [
    path('upload', UploadFile.as_view()),
    path('', GroupList.as_view()),
    path('detail/<int:pk>/', GroupDetail.as_view(), name='group-detail'),
    path('<int:group_id>/members/', GroupMemberList.as_view(), name='group-member-list'),
    path('<int:group_id>/members/<int:pk>/', GroupMemberDetail.as_view(), name='group-member-detail'),
    path('<int:group_id>/messages/', MessageList.as_view(), name='message-list'),
    path('<int:group_id>/messages/<int:pk>/', MessageDetail.as_view(), name='message-detail'),
    path('<int:group_id>/documents/', DocumentList.as_view(), name='document-list'),
    path('<int:group_id>/documents/<int:pk>/', DocumentDetail.as_view(), name='document-detail'),
    path('<int:group_id>/progress/', ProgressDetail.as_view(), name='progress-detail'),
    path('getid/<int:task_id>/', getid.as_view(), name='getid'),
    path('groupLeader/<int:group_id>', groupLeader.as_view(), name="groupLeader"),
    path('groupget/<int:pk>', groupget.as_view(), name="groupget"),
    path('<str:imgurl>', GetImage.as_view()),
]