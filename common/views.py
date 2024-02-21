from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification, User
from group.models import Group
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404


class NotificationListView(APIView):
    def get(self, request, user_id):
        # 获取当前用户的所有通知
        user = get_object_or_404(User, id=user_id)
        notifications = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notifications, many=True)
        response_data = {
            'user_id': user_id,
            'notifications': serializer.data
        }
        return Response(response_data)


class NotificationDetailView(APIView):
    def get(self, request, user_id, notification_id):
        # 获取指定通知的详细信息
        user = get_object_or_404(User, id=user_id)
        notification = get_object_or_404(Notification, id=notification_id, user=user)
        serializer = NotificationSerializer(notification)
        notification.is_read = True
        notification.save()
        return Response(serializer.data)


class NotificationCreateView(APIView):
    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        users = group.members.all()

        # 创建包含所有用户 ID 的数据
        data = {
            'user_ids': [user.id for user in users],
            'title': request.data.get('title'),
            'message': request.data.get('message')
        }

        serializer = NotificationSerializer(data=data, context={'group_id': group_id})
        if serializer.is_valid():
            notifications = serializer.save()
            response_data = {
                'group_id': group_id,
                'notifications': notifications
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)