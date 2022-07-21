from rest_framework import serializers

from Page.models import *


class PageAdminOrModerSerializer(serializers.ModelSerializer):
    unblock_date = serializers.DateTimeField(default=None)

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers',
                  'image', 'is_private', 'follow_requests', 'liked_posts', 'unblock_date')

        def update(self, instance, validated_data):
            if validated_data['unblock_date']:
                instance.unblock_date = validated_data['unblock_date']
                instance.save()
                validated_data.pop('unblock_date')
            return instance


class PageUserSerializer(serializers.ModelSerializer):
    unblock_date = serializers.DateTimeField(default=None)

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers',
                  'image', 'is_private', 'follow_requests', 'liked_posts', 'unblock_date')
        read_only_fields = ('unblock_date', 'owner')


class PageModelFollowRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('follow_requests', 'followers')

    def update(self, instance, validated_data):
        # updating accepted requests
        if validated_data.get('accept_ids', False):
            instance.followers.add(*validated_data['accept_ids'])
            if instance.follow_requests:
                instance.follow_requests.remove(*validated_data['accept_ids'])
        # updating denied requests
        if validated_data.get('deny_ids', False) and instance.follow_requests:
            instance.follow_requests.remove(*validated_data['deny_ids'])
        instance.save()
        return instance


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
