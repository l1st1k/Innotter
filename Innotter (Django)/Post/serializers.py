from rest_framework import serializers

from .models import Post


class PostModelSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        extra_fields = ['likes']
        extra_kwargs = {
            'pages_that_liked': {'read_only': True},
        }

    def get_likes(self, obj):
        """
        Counting amount of likes
        """
        return obj.pages_that_liked.count()
