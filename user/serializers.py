from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, EducationOrWorkInfo, UserCredit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'name', 'email']


class EducationOrWorkInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EducationOrWorkInfo
        fields = ['user', 'school_or_company', 'major_or_department', 'class_or_position']


class UserCreditSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserCredit
        fields = ['user', 'credit']
