from rest_framework import serializers
from django.contrib.auth.models import User
from task.models import Task  # 假设 Task 模型来自 task app
from user.models import UserCredit  # 假设 UserCredit 模型来自 user app
from .models import TaskSettlement, MemberContribution


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserCreditSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserCredit
        fields = ['user', 'credit']


class TaskSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'detail', 'type', 'leader', 'deadline']


class TaskSettlementSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskSettlement
        fields = ['task', 'is_completed', 'completion_time']


class MemberContributionSerializer(serializers.ModelSerializer):
    settlement = TaskSettlementSerializer(read_only=True)
    member = UserSerializer(read_only=True)

    class Meta:
        model = MemberContribution
        fields = ['settlement', 'member', 'contribution']
