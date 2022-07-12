from rest_framework import serializers
from User.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'title', 'is_blocked', 'followed_pages', 'requested_pages',
                  'image_s3_path']
