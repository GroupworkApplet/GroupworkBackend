from django.db import transaction
from django.http import Http404
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TaskProgress, TaskAssignment, Task, ClockIn
from .serializers import TaskProgressSerializer, TaskAssignmentSerializer, TaskSerializer, TaskClockInSerializer


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


class getClockInfo(views.APIView):
    def get(self, request):
        taskId = request.GET.get('task_id')
        # list = ClockIn.objects.filter(task_id=taskId)
        # serialized_data = [TaskClockInSerializer(clock_in).data for clock_in in list]
        # return JsonResponse(serialized_data, safe=False)

        try:
            clockIn = get_list_or_404(ClockIn, task_id=taskId)
        except Http404:
            clockIn = []
        serializer = TaskClockInSerializer(clockIn, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # serializer = TaskClockInSerializer(data=request.data)
        # ClockIn.objects.create(**request.data)
        # # if serializer.is_valid():
        # #     ClockIn.objects.create(uid=serializer.validated_data['uid'],uname=serializer.validated_data['uname'],text=serializer.validated_data['text'],img_url=serializer.validated_data['img_url'],task_id=serializer.validated_data['task_id'],group_id=serializer.validated_data['group_id'])
        # return JsonResponse(request.data, safe=False)
        serializer = TaskClockInSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
