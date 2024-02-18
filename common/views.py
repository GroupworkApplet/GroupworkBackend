from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404


class NotificationListView(APIView):
    def get(self, request):
        # 获取当前用户的所有通知
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationDetailView(APIView):
    def get(self, request, notification_id):
        # 获取指定通知的详细信息
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        serializer = NotificationSerializer(notification)
        notification.is_read = True
        notification.save()
        return Response(serializer.data)
