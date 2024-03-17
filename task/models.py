from django.contrib.auth.models import User
from django.db import models


# 任务表：存储任务的基本信息，如名称、详情、类型、创建者、截止日期等。
# 任务分配表：记录任务发起者和参与者（团队成员）之间的关系，以及各成员的工作栏目。
# 任务进度表：记录任务的进度，任务的状态，以及提醒时间、提醒内容等。

# 任务模型
class Task(models.Model):
    TYPE_CHOICES = [
        ('0', '微视频'),
        ('1', 'PRE'),
        ('2', '演讲'),
        ('3', '社会实践'),
        ('4', '辩论'),
        ('5', '其他'),
    ]

    title = models.CharField(max_length=50, verbose_name='任务名称')
    detail = models.TextField(verbose_name='任务详情',blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='任务类型')
    number=models.CharField(verbose_name="小组人数",max_length=2,default="")
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader', verbose_name='任务创建者')
    deadline = models.CharField(max_length=20,verbose_name='截止日期')

    def __str__(self):
        return self.title


# 任务分配模型
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments', verbose_name='任务')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments', verbose_name='任务参与者',
                                blank=True, null=True, default=None)
    content = models.TextField(max_length=100, verbose_name='任务内容', default='', blank=True, null=True)

    def __str__(self):
        return f"{self.task.title} - {self.partner.username}"


# 任务进度模型
class TaskProgress(models.Model):
    STATUS_CHOICES = [
        ('0', '未开始'),
        ('1', '进行中'),
        ('2', '已完成'),
    ]

    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='progress', verbose_name='任务')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='任务状态')
    remind_time = models.CharField(verbose_name='提醒时间',blank=True,max_length=20)
    remind_content = models.TextField(verbose_name='提醒内容',blank=True)

    def __str__(self):
        return f"{self.task.title} - {self.status}"


class ClockIn(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    uid = models.IntegerField()
    uname = models.CharField(max_length=20)
    text = models.TextField()
    img_url = models.CharField(max_length=100)
    task_id = models.IntegerField()
    group_id = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.uid} - {self.uname} - {self.text} - {self.img_url} - {self.task_id} - {self.group_id} - {self.created_time}"
