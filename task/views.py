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
                    'remind_time': "2024-1-1",
                    'remind_content': "quick"
                }
                task_progress_serializer = TaskProgressSerializer(data=task_progress_data)
                if task_progress_serializer.is_valid():
                    task_progress = task_progress_serializer.save()
                else:
                    return Response(task_progress_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # 合并任务和任务进度的数据，并返回
                response_data = {
                    'task': task_serializer.data,
                    'task_progress': task_progress_serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 获取某人领导的所有任务
class TaskFound(APIView):
    def get(self, request, pk):
        tasks = Task.objects.filter(leader=pk)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


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
        # 首先获取 Task 对象
        task = get_object_or_404(Task, pk=pk)
        # 然后获取关联的 TaskProgress 对象
        task_progress = get_object_or_404(TaskProgress, task=task)
        serializer = TaskProgressSerializer(task_progress)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task_progress = get_object_or_404(TaskProgress, task=task)
        serializer = TaskProgressSerializer(task_progress, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 任务分配表
class TaskAssignmentList(APIView):
    def post(self, request, pk):
        # 获取任务对象
        task = get_object_or_404(Task, pk=pk)
        # 创建任务分配的序列化器，并传递任务对象到context参数中
        serializer = TaskAssignmentSerializer(data=request.data, context={'task': task})
        if serializer.is_valid():
            task_assignment = serializer.save()
            task_id = task_assignment.task_id
            response_data = {
                'task_assignment': serializer.data,
                'task_id': task_id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        # 获取任务对象
        task = get_object_or_404(Task, pk=pk)
        # 获取任务分配列表
        task_assignments = task.assignments.all()
        serializer = TaskAssignmentSerializer(task_assignments, many=True)
        task_id = task_assignments[0].task_id
        response_data = {
            'task_assignments': serializer.data,
            'task_id': task_id
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, pk, assignment_id):
        # 获取任务对象和任务分配对象
        task = get_object_or_404(Task, pk=pk)
        task_assignment = get_object_or_404(TaskAssignment, pk=assignment_id, task=task)

        # 更新任务分配的序列化器
        serializer = TaskAssignmentSerializer(task_assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, assignment_id):
        # 获取任务对象和任务分配对象
        task = get_object_or_404(Task, pk=pk)
        task_assignment = get_object_or_404(TaskAssignment, pk=assignment_id, task=task)

        # 删除任务分配
        task_assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
