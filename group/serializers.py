from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class GroupSerializer(serializers.ModelSerializer):
    task = serializers.CharField(source='task.title')
    members = serializers.StringRelatedField(many=True)

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('created_at',)


class GroupMemberSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    user = serializers.CharField(source='user.name')

    class Meta:
        model = GroupMember
        fields = '__all__'
        read_only_fields = ('is_leader', 'joined_at',)


class MessageSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    sender = serializers.CharField(source='user.name')

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('created_at',)


class DocumentSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    sender = serializers.CharField(source='user.name')

    class Meta:
        model = Document
        fields = '__all__'


class ProgressSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')

    class Meta:
        model = Progress
        fields = '__all__'
