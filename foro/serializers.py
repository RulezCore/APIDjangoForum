from rest_framework import serializers
from .models import Profile, Category, Topic, ResponseTopic
from django.contrib.auth.models import User

# C:\Users\RulezCore\.virtualenvs\Backend-ROwmHwsW\Scripts\python.exe

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_active', 'user_permissions')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'birth_date', 'profilePic')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'description')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('title', 'description', 'fixed')

class TopicDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    user = ProfileSerializer()

    class Meta:
        model = Topic
        fields = ('title', 'description', 'fixed', 'category', 'user')