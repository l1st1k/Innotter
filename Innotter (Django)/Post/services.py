from django.db.models import F
from .models import Post


def add_like_to_post(post):
    pass
    # Нужно добавить лайк во все другие поля
    # post.likes = F('likes') + 1
    # post.save()