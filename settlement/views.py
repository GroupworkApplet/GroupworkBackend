from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import TaskSettlement, MemberContribution, UserCredit

def show_results(request):
    # 获取任务完成情况并计算成员贡献率
    settlements = TaskSettlement.objects.filter(is_completed=True)
    members_contribution = {}
    total_tasks_completed = settlements.count()

    for settlement in settlements:
        contributions = MemberContribution.objects.filter(settlement=settlement)
        for contribution in contributions:
            member_username = contribution.member.username
            members_contribution[member_username] = members_contribution.get(member_username, 0) + contribution.contribution

    # 计算贡献率
    for member, contribution in members_contribution.items():
        members_contribution[member] = (contribution / total_tasks_completed) * 100

    # 渲染模板并传递贡献率数据
    return render(request, 'results.html', {'members_contribution': members_contribution})

def handle_timeout(request):
    # 处理超时或未完成任务的成员
    settlements = TaskSettlement.objects.filter(is_completed=False)
    for settlement in settlements:
        if settlement.completion_time and settlement.completion_time > settlement.task.deadline:
            contributions = MemberContribution.objects.filter(settlement=settlement)
            for contribution in contributions:
                user_credit, created = UserCredit.objects.get_or_create(user=contribution.member)
                user_credit.credit -= 10
                user_credit.save()

    return JsonResponse({'message': 'Timeout handled successfully'})

def adjust_contribution(request, member_id):
    # 根据完成情况调整成员的贡献值
    member = User.objects.get(id=member_id)
    contributions = MemberContribution.objects.filter(member=member)
    for contribution in contributions:
        if contribution.settlement.is_completed:
            if contribution.settlement.completion_time and contribution.settlement.completion_time > contribution.settlement.task.deadline:
                contribution.contribution -= 10  # 如果任务超时完成，减少贡献值
            else:
                contribution.contribution += 5  # 任务按时完成，增加贡献值
            contribution.save()

    return JsonResponse({'message': 'Contribution adjusted successfully'})
