from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
    followed_pages = models.ManyToManyField('Page.Page', related_name='followed_pages', null=True, blank=True)
    requested_pages = models.ManyToManyField('Page.Page', related_name='requested_pages', null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']


class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    refresh_token = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    exp_time = models.IntegerField()  # in days
