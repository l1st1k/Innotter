import boto3
from dotenv import dotenv_values
from Page.models import Page
from Innotter.celery import app

config = dotenv_values("/usr/src/app/.env")
S3_ENDPOINT = config["S3_ENDPOINT"]
AWS_ACCESS_KEY = config["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
MAIL_SENDER = config["SES_MAIL_SENDER"]
AWS_REGION_NAME = config["AWS_REGION_NAME"]


def send_emails(post):
    mail_data = prepared_data(post)

    celery_send_emails.delay(*mail_data)


def prepared_data(post):
    page = Page.objects.prefetch_related('followers').get(pk=post.page.id)
    followers_list = list(page.followers.values_list('email', flat=True))
    page_name = page.name
    post_url = f'http://innotter/api/v1/posts/{post.id}/'
    return followers_list, page_name, post_url


@app.task()
def celery_send_emails(followers_list, page_name, post_url):
    send_emails_from_ses(followers_list, page_name, post_url)


def send_emails_from_ses(followers_list, page_name, post_url):
    ses = boto3.client("ses", endpoint_url=S3_ENDPOINT, aws_access_key_id=AWS_ACCESS_KEY,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)
    ses.verify_email_identity(EmailAddress=MAIL_SENDER)
    ses.send_email(
            Destination={
                "ToAddresses": followers_list
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": f"Checkout new post on {page_name}:\n"
                                f"{post_url}",
                    }
                },
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": "New Post!",
                },
            },
            Source=MAIL_SENDER
        )
