from rest_framework import serializers
from user.serializers import UserSerializer
from django.contrib.auth.models import User
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'created_time', 'is_read']

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids', [])
        group = self.context.get('group')
        notifications = []

        for user_id in user_ids:
            notification_data = {
                **validated_data,
                'user_id': user_id,
                'group': group
            }
            notifications.append(Notification.objects.create(**notification_data))

        return notifications


