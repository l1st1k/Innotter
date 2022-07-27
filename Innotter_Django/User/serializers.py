from rest_framework import serializers

from .models import User
from .services import block_all_users_pages, unblock_all_users_pages


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'title', 'image_s3_path', 'role', 'is_blocked',
                  'followed_pages', 'requested_pages')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('followed_pages', 'requested_pages')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            role='user',
            title=validated_data['title'],
            is_blocked=False,
            image_s3_path=validated_data['image_s3_path']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        # validated_data.pop('password')
        instance.email = validated_data.get('email', instance.email)
        instance.title = validated_data.get('title', instance.title)
        instance.image_s3_path = validated_data.get('image_s3_path', instance.image_s3_path)
        instance.role = validated_data.get('role', instance.role)
        instance.is_blocked = validated_data.get('is_blocked', instance.is_blocked)
        instance.save()
        if instance.role == 'admin':
            instance.is_staff = True
            instance.is_superuser = True
        if instance.is_blocked:
            block_all_users_pages(instance)
        else:
            unblock_all_users_pages(instance)
        return instance
