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

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 需要确保将消息和当前用户关联起来
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class NotificationDetailView(APIView):
    def get(self, request, notification_id):
        # 获取指定通知的详细信息
        notification = get_object_or_404(Notification, id=notification_id)
        if notification.user != request.user:
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = NotificationSerializer(notification)
        notification.is_read = True
        notification.save()
        return Response(serializer.data)

