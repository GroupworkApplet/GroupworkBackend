from django.urls import path
from .views import TaskSettlementView, MemberContributionView, UpdateCreditView

urlpatterns = [
    path('task/<int:task_id>/', TaskSettlementView.as_view()),
    path('contribution/<int:settlement_id>/', MemberContributionView.as_view()),
    path('contribution/update/<int:contribution_id>/', UpdateCreditView.as_view()),
]
