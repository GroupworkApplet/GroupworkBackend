from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile, EducationOrWorkInfo, UserCredit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserCredit.objects.create(user=user, credit=100)
        UserProfile.objects.create(user=user, name=validated_data['username'])
        EducationOrWorkInfo.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"


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