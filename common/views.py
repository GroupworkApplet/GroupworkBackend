from django.shortcuts import render, get_object_or_404
from .models import Notification


# Create your views here.
def notification_list(request):
    notifications = Notification.objects.fliter(user=request.user)
    return render(request, 'notification_list.html', {'通知': notifications})


def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return render(request, 'notification_detail.html', {'通知具体内容': notification})
