from django.shortcuts import render, HttpResponse, redirect
from .models import TaskProgress, TaskAssignment, Task
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TaskDetailsView(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        context = {
            '任务名称': task.title,
            '任务详情': task.detail,
            '任务类型': task.type,
            '任务创建者': task.leader,
            '截止日期': task.deadline
        }
        return Response(context)


class TaskProgressDetailsView(APIView):
    def get(self, request, pk):
        task_progress = get_object_or_404(TaskProgress, pk=pk)
        context = {
            '任务': task_progress.task,
            '任务状态': task_progress.status,
            '提醒时间': task_progress.remind_time,
            '提醒内容': task_progress.remind_content
        }
        return Response(context)


# 任务分配
class TaskAssignmentList(APIView):
    def get(self, request):
        task_assignments = TaskAssignment.objects.all()
        data = []
        for assignment in task_assignments:
            data.append({
                'task_id': assignment.task_id,
                'task_title': assignment.task.title,
                'partner_id': assignment.partner_id,
                'partner_username': assignment.partner.username
            })
        return Response(data)

    def post(self, request):
        task_id = request.data.get('task_id')
        partner_id = request.data.get('partner_id')

        try:
            task_assignment = TaskAssignment.objects.create(task_id=task_id, partner_id=partner_id)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TaskAssignmentDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(TaskAssignment, pk=pk)

    def get(self, request, pk):
        task_assignment = self.get_object(pk)
        data = {
            'task_id': task_assignment.task_id,
            'task_title': task_assignment.task.title,
            'partner_id': task_assignment.partner_id,
            'partner_username': task_assignment.partner.username
        }
        return Response(data)

    def put(self, request, pk):
        task_assignment = self.get_object(pk)
        task_id = request.data.get('task_id')
        partner_id = request.data.get('partner_id')

        try:
            task_assignment.task_id = task_id
            task_assignment.partner_id = partner_id
            task_assignment.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task_assignment = self.get_object(pk)
        task_assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
