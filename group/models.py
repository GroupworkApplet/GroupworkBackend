from django.contrib.auth.models import User
from django.db import models


from task.models import Task

#小组的类
class GroupList(models.Model):
    group_name = models.CharField(max_length=10, verbose_name='小组名')
    task = models.OneToOneField(Task, verbose_name='对应任务', on_delete=models.CASCADE)
    group_members = models.ManyToManyField(User)

# Create your models here.
