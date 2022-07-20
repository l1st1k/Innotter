from django.db.models import F
from .models import Post
from Page.models import Page
from User.models import User


def add_like_to_post(post):
    pass
    # Нужно добавить лайк во все другие поля
    # post.likes = F('likes') + 1
    # post.save()


def user_is_able_to_see_the_post(user, post):
    page = Page.objects.get(pk=post.page.id)
    return (not page.is_private) or (page.owner == user) or (user.role == User.Roles.ADMIN) or\
           (user.role == User.Roles.MODERATOR) or (user.id in page.followers)


def user_is_page_owner(user, page_id):
    page = Page.objects.get(id=page_id)
    return page.owner == user
