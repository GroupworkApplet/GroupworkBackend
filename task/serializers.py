from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Task, TaskAssignment, TaskProgress


class TaskSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'detail', 'type', 'leader', 'deadline']


class TaskAssignmentSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    partner = UserSerializer(read_only=True)

    class Meta:
        model = TaskAssignment
        fields = ['id', 'task', 'partner']


class TaskProgressSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskProgress
        fields = ['id', 'task', 'status', 'remind_time', 'remind_content']
