from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
