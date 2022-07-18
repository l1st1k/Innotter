from django.utils import timezone
# from django.db.models import F
# from .models import Page


def is_page_unblocked(unblock_date):
    return timezone.now() >= unblock_date

