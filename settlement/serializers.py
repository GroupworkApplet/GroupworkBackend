from rest_framework import serializers
from user.serializers import UserSerializer
from django.contrib.auth.models import User
from task.models import Task
from user.models import UserCredit
from .models import TaskSettlement, MemberContribution


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
