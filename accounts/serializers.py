
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'role']

    @transaction.atomic
    def create(self, validated_data):

        phone = validated_data.pop('phone', '')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        Profile.objects.create(
            user=user,
            phone=phone,
            role='end_user'
        )

        return user

    def get_role(self, obj):
        return obj.profile.role


class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'role', 'phone', 'created_at']
