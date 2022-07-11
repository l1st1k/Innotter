from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('Page.Tag', related_name='tags')
    owner = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('User.User', related_name='followers')
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('User.User', related_name='follow_requests')
    unblock_date = models.DateTimeField(null=True, blank=True)
