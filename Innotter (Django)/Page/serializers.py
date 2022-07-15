from rest_framework import serializers
from Page.models import *


class PageAdminOrModerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('username', 'password', 'email', 'title', 'image_s3_path', 'role', 'is_blocked',
                  'followed_pages', 'requested_pages')


class PageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('username', 'password', 'email', 'title', 'image_s3_path', 'role', 'is_blocked',
                  'followed_pages', 'requested_pages')


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
