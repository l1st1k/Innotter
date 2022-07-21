from django.utils import timezone


def is_page_unblocked(unblock_date):
    return timezone.now() >= unblock_date


def add_follow_requests_to_request_data(request_data, follow_requests):
    # taking all the User's ids
    follow_requests = list(follow_requests.values_list('pk', flat=True))
    # adding them to request data
    request_data.update({'follow_requests': follow_requests})
    return request_data


def user_is_in_page_follow_requests_or_followers(user, page):
    return page.follow_requests.filter(id=user.pk).exists() or page.followers.filter(id=user.pk).exists()


def add_user_to_page_follow_requests(user, page):
    page.follow_requests.add(user)


def add_user_to_page_followers(user, page):
    page.followers.add(user)
