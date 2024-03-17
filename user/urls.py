from django.urls import path

from .views import (UserRegisterView, UserLoginView, UserLogoutView, UserProfileUpdateView,
                    UserEducationOrWorkInfoUpdateView, UserCreditView, jwtorder, Userinfoget, Eduget)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:pk>', UserProfileUpdateView.as_view(), name='user_profile'),
    path('education_or_work_info/<int:pk>', UserEducationOrWorkInfoUpdateView.as_view(), name='education_or_work_info'),
    path('credit/', UserCreditView.as_view(), name='user_credit'),
    path('prove/', jwtorder.as_view(), name='jwtorder'),
    path('Userinfoget/<int:pk>', Userinfoget.as_view(), name='Usergetinfo'),
    path('eduget/<int:pk>', Eduget.as_view(), name="Eduget")
]
