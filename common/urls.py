from django.urls import path
from .views import NotificationListView, NotificationDetailView, NotificationCreateView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:user_id>/<int:notification_id>/',
         NotificationDetailView.as_view(),
         name='notification-detail'),
    path('notifications/<int:group_id>/', NotificationCreateView.as_view(), name='notification-create'),
]

