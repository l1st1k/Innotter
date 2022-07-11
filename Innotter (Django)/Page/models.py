from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=80, unique=True)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('Page.Tag', related_name='tags', blank=True)
    owner = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('User.User', related_name='followers', null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('User.User', related_name='follow_requests', null=True, blank=True)
    liked_posts = models.ManyToManyField('Post.Post', related_name='liked_posts', null=True, blank=True)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
