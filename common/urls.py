from django.urls import path
from .views import notification_list, notification_detail

urlpatterns = [
    path('notifications/', notification_list),
    path('notifications/<int:pk>/', notification_detail),
]



