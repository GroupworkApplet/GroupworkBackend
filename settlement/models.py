from django.db import models
from django.contrib.auth.models import User

from user.models import UserCredit


# 任务结算
class TaskSettlement(models.Model):
    task = models.OneToOneField('task.Task', on_delete=models.CASCADE, related_name='settlement', verbose_name='任务')
    is_completed = models.BooleanField(default=False, verbose_name='是否完成')
    completion_time = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')

    def __str__(self):
        return f"{self.task.title} - {'已完成' if self.is_completed else '未完成'}"


# 成员贡献
class MemberContribution(models.Model):
    settlement = models.ForeignKey(TaskSettlement, on_delete=models.CASCADE, related_name='contributions', verbose_name='结算')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions', verbose_name='成员')
    contribution = models.FloatField(verbose_name='贡献值')

    def __str__(self):
        return f"{self.settlement.task.title} - {self.member.username} - {self.contribution}"

    def update_credit(self, *args, **kwargs):
        super(MemberContribution, self).save(*args, **kwargs)
        user_credit, created = UserCredit.objects.get_or_create(user=self.member)

        if self.settlement.is_completed:
            credit_update = 5
        else:
            credit_update = -10

        user_credit.credit += credit_update
        user_credit.save()
