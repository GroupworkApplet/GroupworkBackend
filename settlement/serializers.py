from rest_framework import serializers
from .models import TaskSettlement, MemberContribution, User


class TaskSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSettlement
        fields = ['is_completed', 'completion_time']

    def create(self, validated_data):
        task = self.context.get('task')
        validated_data['task'] = task
        settlement = TaskSettlement.objects.create(**validated_data)
        return settlement


class MemberContributionSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = MemberContribution
        fields = ['member', 'contribution']

    def create(self, validated_data):
        settlement = self.context['settlement']
        member = validated_data['member']
        contribution = validated_data.get('contribution', 0)

        member_contribution = MemberContribution.objects.create(
            settlement=settlement,
            member=member,
            contribution=contribution
        )

        member_contribution.update_credit()
        return member_contribution

