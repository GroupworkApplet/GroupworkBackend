from django.urls import path
from .views import TaskSettlementView, MemberContributionView

urlpatterns = [
    path('task/<int:task_id>/', TaskSettlementView.as_view()),
    path('contribution/<int:task_id>/', MemberContributionView.as_view()),
]
