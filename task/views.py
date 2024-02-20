from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect
from .models import TaskProgress, TaskAssignment, Task
from .serializers import TaskProgressSerializer, TaskAssignmentSerializer, TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# 创建任务
class CreateTaskView(APIView):
    def post(self, request):
        with transaction.atomic():
            # 创建任务
            task_serializer = TaskSerializer(data=request.data)
            if task_serializer.is_valid():
                task = task_serializer.save()

                # 创建任务进度，默认状态为"未开始"
                task_progress_data = {
                    'task': task.id,
                    'status': '0',
                    'remind_time': None,
                    'remind_content': ''
                }
                task_progress_serializer = TaskProgressSerializer(data=task_progress_data)
                if task_progress_serializer.is_valid():
                    task_progress_serializer.save()
                else:
                    return Response(task_progress_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(task_serializer.data, status=status.HTTP_201_CREATED)
            return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 任务详情
class TaskDetailsView(APIView):
    def get(self, request, pk):
        # 获取任务详情
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        # 更新任务详情
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # 删除任务
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 任务进度
class TaskProgressDetailsView(APIView):
    def get(self, request, pk):
        # 获取任务进度详情
        task_progress = get_object_or_404(TaskProgress, pk=pk)
        serializer = TaskProgressSerializer(task_progress)
        return Response(serializer.data)

    def put(self, request, pk):
        # 更新任务进度详情
        task_progress = get_object_or_404(TaskProgress, pk=pk)
        serializer = TaskProgressSerializer(task_progress, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 任务分配表
class TaskAssignmentList(APIView):
    def get(self, request):
        # 获取任务分配
        task_assignments = TaskAssignment.objects.all()
        serializer = TaskAssignmentSerializer(task_assignments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 创建任务分配
        serializer = TaskAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 任务分配详情
class TaskAssignmentDetail(APIView):
    def get_object(self, pk):
        # 获取任务分配对象
        return get_object_or_404(TaskAssignment, pk=pk)

    def get(self, request, pk):
        # 获取任务分配详情
        task_assignment = self.get_object(pk)
        serializer = TaskAssignmentSerializer(task_assignment)
        return Response(serializer.data)

    def put(self, request, pk):
        # 更新任务分配详情
        task_assignment = self.get_object(pk)
        serializer = TaskAssignmentSerializer(task_assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # 删除任务分配
        task_assignment = self.get_object(pk)
        task_assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
