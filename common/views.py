from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification, User
from group.models import Group
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404


class NotificationListView(APIView):
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationDetailView(APIView):
    def get(self, request, notification_id):
        user = request.user
        notification = get_object_or_404(Notification, id=notification_id, user=user)
        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class NotificationCreateView(APIView):
    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        users = group.members.all()

        data = {
            'user_ids': [user.id for user in users],
            'title': request.data.get('title'),
            'message': request.data.get('message')
        }

        serializer = NotificationSerializer(data=data, context={'group': group})
        if serializer.is_valid():
            notifications = serializer.save()
            response_data = {
                'notification_ids': [notification.id for notification in notifications],
                'members': [user.id for user in users],
                'group_id': group_id,
                'notifications': NotificationSerializer(notifications, many=True).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
