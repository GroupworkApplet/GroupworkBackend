from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import UserProfile, EducationOrWorkInfo, UserCredit
from .serializers import UserSerializer, UserProfileSerializer, EducationOrWorkInfoSerializer, UserCreditSerializer
from django.views.decorators.csrf import csrf_exempt


# 用户注册

class UserRegisterView(views.APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        # 当数据有效且用户名未注册时，保存用户数据
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if User.objects.filter(username=username).exists():
                return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 用户登录

class UserLoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': '请提供用户名和密码'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'error': '无效的凭证'},
                            status=status.HTTP_404_NOT_FOUND)
        # login(request, user)
        import jwt
        import datetime
        salt = 'asdfghjkl123qwe'
        # 构造header
        header = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        # 构造payload
        payload = {
            'user_id': user.id,
            'user_name': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        result = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=header)
        return Response({'code': 200, 'date': result})


from auth import jwtauthen


class jwtorder(views.APIView):
    authentication_classes = [jwtauthen, ]

    def get(self, request, *args, **kwargs):
        return Response({'code': 200, 'data': request.user})


# 用户登出
class UserLogoutView(views.APIView):
    def get(self, request):
        logout(request)
        return Response({'message': '登出成功'}, status=status.HTTP_200_OK)


# 用户信息更新
class UserProfileUpdateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 用户教育或工作信息更新
class UserEducationOrWorkInfoUpdateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        education_or_work_info = get_object_or_404(EducationOrWorkInfo, user=user)
        serializer = EducationOrWorkInfoSerializer(education_or_work_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 用户信用信息获取和更新
class UserCreditView(views.APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_credit = get_object_or_404(UserCredit, user=user)
        serializer = UserCreditSerializer(user_credit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        user_credit = get_object_or_404(UserCredit, user=user)
        serializer = UserCreditSerializer(user_credit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
