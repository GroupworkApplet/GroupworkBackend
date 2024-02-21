from django.contrib.auth.models import User
from django.db import models
from group.models import Group


# Create your models here.
# 通知
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
