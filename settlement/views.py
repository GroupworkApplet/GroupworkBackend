from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TaskSettlement, MemberContribution
from .serializers import TaskSettlementSerializer, MemberContributionSerializer


class TaskSettlementView(APIView):
    def get(self, request, task_id):
        try:
            settlement = TaskSettlement.objects.get(task_id=task_id)
            serializer = TaskSettlementSerializer(settlement)
            return Response(serializer.data)
        except TaskSettlement.DoesNotExist:
            return Response({'错误': '任务不存在'}, status=status.HTTP_404_NOT_FOUND)


class MemberContributionView(APIView):
    def get(self, request, settlement_id):
        contributions = MemberContribution.objects.filter(settlement_id=settlement_id)
        serializer = MemberContributionSerializer(contributions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MemberContributionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCreditView(APIView):
    def post(self, request, contribution_id):
        try:
            contribution = MemberContribution.objects.get(id=contribution_id)
            contribution.update_credit()
            return Response({'提示': '信用分更新成功'})
        except MemberContribution.DoesNotExist:
            return Response({'错误': '成员贡献不存在'}, status=status.HTTP_404_NOT_FOUND)
