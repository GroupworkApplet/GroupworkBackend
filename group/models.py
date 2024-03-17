from django.contrib.auth.models import User
from django.db import models

from task.models import Task


# 小组的类
class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='小组名')
    task = models.OneToOneField(Task, verbose_name='对应任务', on_delete=models.CASCADE, related_name='task')
    description = models.TextField(verbose_name='小组描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # members = models.ManyToManyField("GroupMember",related_name='groups')
    def __str__(self):
        return self.name


# 小组成员的类
class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members', verbose_name='小组')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_member', verbose_name='用户')
    is_leader = models.BooleanField(default=False, verbose_name='是否为组长')
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')

    def __str__(self):
        return f"{self.group.name} - {self.user.username}"


# 消息的类
class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages', verbose_name='小组')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages', verbose_name='发送者')
    content = models.TextField(verbose_name='消息内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    def __str__(self):
        return f"{self.group.name} - {self.sender.username}"


# 小组文件的类
class Document(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='documents', verbose_name='小组')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', verbose_name='上传者')
    title = models.CharField(max_length=255, verbose_name='文件名')
    file = models.FileField(upload_to='documents/', verbose_name='文件')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    def __str__(self):
        return f"{self.group.name} - {self.title}"


# 任务进度模型
class Progress(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='progress', verbose_name='小组')
    current_progress = models.IntegerField(default=0, verbose_name='当前进度')
    deadline = models.DateTimeField(verbose_name='截止日期')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"{self.group.name} - {self.current_progress}"
