from django.db import models
from django.contrib.auth.models import User


# 用户个人信息
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


# 教育或工作信息
class EducationOrWorkInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education_or_work_info')
    school_or_company = models.CharField(max_length=50)
    major_or_department = models.CharField(max_length=50)
    class_or_position = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.school_or_company}"


# 用户信用分
class UserCredit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credit')
    credit = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.user.username} - {self.credit}"
