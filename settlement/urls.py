from django.urls import path
from .views import show_results, handle_timeout, adjust_contribution

urlpatterns = [
    path('show_results/', show_results),
    path('handle_timeout/', handle_timeout),
    path('adjust_contribution/<int:member_id>/', adjust_contribution),
]