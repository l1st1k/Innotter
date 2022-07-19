from django.utils import timezone
# from django.db.models import F
# from .models import Page


def is_page_unblocked(unblock_date):
    return timezone.now() >= unblock_date


def add_follow_requests_to_request_data(request_data, follow_requests):
    # taking all the User's ids
    follow_requests = list(follow_requests.values_list('pk', flat=True))
    # adding them to request data
    request_data.update({'follow_requests': follow_requests})
    return request_data

