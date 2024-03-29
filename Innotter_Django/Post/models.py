from django.db import models


class Post(models.Model):
    page = models.ForeignKey('Page.Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('Post.Post', on_delete=models.SET_NULL, null=True, related_name='replies', blank=True)
    pages_that_liked = models.ManyToManyField('Page.Page', related_name='pages_that_liked', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
