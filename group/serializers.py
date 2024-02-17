from rest_framework import serializers

from .models import *


class GroupSerializer(serializers.ModelSerializer):
    task_title = serializers.ReadOnlyField(source='task.title')
    members = serializers.PrimaryKeyRelatedField(
        many=True, source='members',
        queryset=GroupMember.objects.all(),
    )
    messages = serializers.PrimaryKeyRelatedField(
        source='messages', many=True, read_only=True
    )
    documents = serializers.PrimaryKeyRelatedField(
        source='documents', many=True, read_only=True
    )
    progress = serializers.PrimaryKeyRelatedField(source='progress',read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class GroupMemberSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')
    user_name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = GroupMember
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')
    sender_name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Message
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')
    sender_name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Document
        fields = '__all__'


class ProgressSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Progress
        fields = '__all__'
