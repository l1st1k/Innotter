from rest_framework import serializers

from .models import Post


class PostModelSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'reply_to', 'created_at', 'updated_at', 'pages_that_liked', 'likes')
        extra_kwargs = {
            'pages_that_liked': {'read_only': True},
        }

    def get_likes(self, obj):
        """
        Counting amount of likes
        """
        if Post.objects.values('pages_that_liked').filter(id=obj.id).first()['pages_that_liked'] is None:
            return 0
        return len(Post.objects.values('pages_that_liked').filter(id=obj.id))
