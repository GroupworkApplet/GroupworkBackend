from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from task.models import Task
from user.models import UserCredit
from .models import TaskSettlement, MemberContribution
from .serializers import TaskSettlementSerializer, MemberContributionSerializer


class TaskSettlementView(APIView):
    def get(self, request, task_id):
        try:
            task = get_object_or_404(Task, pk=task_id)
            settlement = get_object_or_404(TaskSettlement, task=task)
            serializer = TaskSettlementSerializer(settlement)
            response_data = {
                'task_id': task_id,
                'is_completed': serializer.data['is_completed'],
                'completion_time': serializer.data['completion_time']
            }
            return Response(response_data)
        except TaskSettlement.DoesNotExist:
            return Response({'错误': '任务不存在'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskSettlementSerializer(data=request.data, context={'task': task})
        if serializer.is_valid():
            settlement = serializer.save()
            task_id = settlement.task_id
            response_data = {
                'task_id': task_id,
                'is_completed': serializer.data['is_completed'],
                'completion_time': serializer.data['completion_time']
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberContributionView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        settlement = get_object_or_404(TaskSettlement, task=task)
        contributions = MemberContribution.objects.filter(settlement=settlement)
        serializer = MemberContributionSerializer(contributions, many=True)
        response_data = {
            'task_id': task_id,
            'contributions': serializer.data
        }
        return Response(response_data)

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        settlement = get_object_or_404(TaskSettlement, task=task)
        serializer = MemberContributionSerializer(data=request.data, context={'settlement': settlement})
        if serializer.is_valid():
            contribution = serializer.save()
            task_id = contribution.settlement.task_id
            response_data = {
                'task_id': task_id,
                'member': serializer.data['member'],
                'contribution': serializer.data['contribution']
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        settlement = get_object_or_404(TaskSettlement, task=task)
        contributions = MemberContribution.objects.filter(settlement=settlement)

        updated_contributions = []
        for contribution in contributions:
            # 更新每个成员的信用分
            contribution.update_credit()
            updated_contributions.append({
                'member': contribution.member.username,
                'contribution': contribution.contribution,
                'updated_credit': UserCredit.objects.get(user=contribution.member).credit
            })

        return Response({
            'task_id': task_id,
            'updated_contributions': updated_contributions
        }, status=status.HTTP_200_OK)
