from django.contrib.auth.models import User
from django.db import models

# Create your models here.
#通知
class notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField(max_length=100)
    created_time=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    def __str__(self):
        return self.message