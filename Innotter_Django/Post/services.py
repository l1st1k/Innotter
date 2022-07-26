from Page.models import Page
from User.models import User


def add_like_to_post(page_id, post):
    page = Page.objects.get(pk=page_id)
    page.liked_posts.add(post)
    post.pages_that_liked.add(page)
    page.save()
    post.save()


def user_is_able_to_see_the_post(user, post):
    page = Page.objects.get(pk=post.page.id)
    return (not page.is_private) or (page.owner == user) or (user.role == User.Roles.ADMIN) or\
           (user.role == User.Roles.MODERATOR) or (user.id in page.followers)


def user_is_page_owner(user, page_id):
    page = Page.objects.get(id=page_id)
    return page.owner == user


def foreign_page(user, page_id):
    page = Page.objects.get(pk=page_id)
    return page.owner != user
