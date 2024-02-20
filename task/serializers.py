from rest_framework import serializers
from .models import Task, TaskAssignment, TaskProgress


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'detail', 'type', 'leader', 'deadline']


class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = ['id', 'partner', 'content']

    def create(self, validated_data):
        # 从视图的上下文中获取任务对象
        task = self.context.get('task')

        # 将任务对象与任务分配关联起来
        validated_data['task'] = task

        # 创建任务分配对象
        task_assignment = TaskAssignment.objects.create(**validated_data)
        return task_assignment


class TaskProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskProgress
        fields = ['id', 'task', 'status', 'remind_time', 'remind_content']
