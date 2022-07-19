from rest_framework import serializers
from .models import Post


class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'reply_to', 'created_at', 'updated_at', 'pages_that_liked')
        extra_kwargs = {
            'pages_that_liked': {'read_only': True},
        }
