from rest_framework import serializers
from Page.models import *


class PageAdminOrModerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers',
                  'image', 'is_private', 'follow_requests', 'liked_posts', 'unblock_date')


class PageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers',
                  'image', 'is_private', 'follow_requests', 'liked_posts', 'unblock_date')


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
