from rest_framework import serializers
from user.serializers import UserSerializer
from django.contrib.auth.models import User
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'created_time', 'is_read']

    def create(self, validated_data):
        user = validated_data.pop('user_ids', [])
        notifications = []
        group = self.context.get('group')
        validated_data['group'] = group

        for user_id in user:
            notification_data = {
                **validated_data,
                'user': user_id
            }
            notification = Notification.objects.create(**notification_data)
            notifications.append(notification)

        return notifications


