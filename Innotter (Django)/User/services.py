import datetime

import boto3
import botocore
import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from dotenv import dotenv_values

from Innotter import settings
from Page.models import Page
from User.models import RefreshToken

config = dotenv_values("/usr/src/app/.env")
S3_ENDPOINT = config["S3_ENDPOINT"]
AWS_ACCESS_KEY = config["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]


def upload_image_to_s3(image):
    s3 = boto3.client("s3", endpoint_url=S3_ENDPOINT, aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.put_object(Body=image, Bucket='innotter-storage', Key=f'{image}')
    s3_url = 'http://localhost.localstack.cloud:4566/innotter-storage/' + f'{image}'
    return s3_url


def unblock_all_users_pages(user):
    unblock_date = timezone.now()
    Page.objects.filter(owner=user).update(unblock_date=unblock_date)


def block_all_users_pages(user):
    unblock_date = timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
    Page.objects.filter(owner=user).update(unblock_date=unblock_date)


def generate_access_token(user):
    token = jwt.encode({
        'username': user.username,
        'iat': datetime.datetime.utcnow(),
        'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, settings.SECRET_KEY)
    return token


def generate_refresh_token():
    refresh_token = jwt.encode({
        'iat': datetime.datetime.utcnow(),
        'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, settings.SECRET_KEY)
    return refresh_token


def get_refresh_token_obj(refresh_token):
    try:
        old_token = RefreshToken.objects.get(refresh_token=refresh_token)
    except ObjectDoesNotExist:
        return None
    return old_token


def set_refresh_token(refresh_token, user):
    refresh_token = RefreshToken(user=user, refresh_token=refresh_token,
                                 exp_time=settings.CUSTOM_JWT['REFRESH_TOKEN_LIFETIME_MODEL'])
    refresh_token.save()


def check_and_update_refresh_token(refresh_token):
    old_token = get_refresh_token_obj(refresh_token)
    if old_token:
        # checks if refresh_token is still works
        if timezone.now() - datetime.timedelta(days=old_token.exp_time) > old_token.created_at:
            return None
        new_access_token = generate_access_token(old_token.user)
        new_refresh_token = generate_refresh_token()
        set_refresh_token(new_refresh_token, old_token.user)
        old_token.delete()
        return {settings.CUSTOM_JWT['AUTH_COOKIE']: new_access_token,
                settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH']: new_refresh_token}
