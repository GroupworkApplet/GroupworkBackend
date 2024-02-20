from rest_framework import serializers
from user.serializers import UserSerializer
from task.serializers import TaskSerializer
from .models import TaskSettlement, MemberContribution


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
