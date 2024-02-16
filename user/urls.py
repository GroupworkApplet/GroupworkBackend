from django.urls import path
from .views import (UserRegisterView, UserLoginView, UserLogoutView, UserProfileUpdateView,
                    UserEducationOrWorkInfoUpdateView, UserCreditView)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('profile/', UserProfileUpdateView.as_view(), name='user_profile'),
    path('education_or_work_info/', UserEducationOrWorkInfoUpdateView.as_view(), name='education_or_work_info'),
    path('credit/', UserCreditView.as_view(), name='user_credit'),
]
