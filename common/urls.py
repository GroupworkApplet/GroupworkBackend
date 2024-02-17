from django.urls import path
from .views import notification_list, notification_detail

urlpatterns = [
    path("notification_list/", notification_list),
    path("notification_detail/", notification_detail),
]
