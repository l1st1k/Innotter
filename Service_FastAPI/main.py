import requests
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class UserModel(BaseModel):
    username: str = Field(title='Login', max_length=30)
    password: str = Field(title='Password', max_length=30)


class StatsResponseModel(BaseModel):
    page_name: str = Field(title='Page name', max_length=80)
    page_id: int = Field(title='Page ID', ge=0)
    amount_of_posts: int = Field(title='Amount of posts', ge=0)
    amount_of_followers: int = Field(title='Amount of followers', ge=0)
    amount_of_likes: int = Field(title='Amount of likes', ge=0)


def get_tokens_for_cookies(login, password):
    headers = {"accept": "application/json"}
    data = {
        "username": login,
        "password": password
    }
    response = requests.post(f"http://localhost:8000/api/v1/token/create/", headers=headers, data=data)
    return response.json()


def get_amount_of_likes(posts) -> int:
    counter = 0
    for post in posts:
        counter += int(post['likes'])
    return counter


def get_request_to_django_page(page_id: int, cookies: dict, url: str):
    headers = {"Authorization": f"Bearer {cookies['access_token']}", "Content-Type": "application/json"}
    url = url.replace('{page_id}', str(page_id))
    response = requests.get(url=url, headers=headers, cookies=cookies)
    return response


@app.post("/api/v1/page/{page_id}/stats", response_model=StatsResponseModel, name='Page stats by ID')
async def stats(page_id: int, user: UserModel):
    cookies = get_tokens_for_cookies(user.username, user.password)
    response_name = get_request_to_django_page(page_id=page_id, cookies=cookies,
                                               url="http://localhost:8000/api/v1/page/{page_id}/")
    page_name = response_name.json()["name"]

    response_followers = get_request_to_django_page(page_id=page_id, cookies=cookies,
                                                    url="http://localhost:8000/api/v1/page/{page_id}/followers/")
    amount_of_followers = len(response_followers.json()['followers'])

    response_posts = get_request_to_django_page(page_id=page_id, cookies=cookies,
                                                url="http://localhost:8000/api/v1/page/{page_id}/posts/")
    amount_of_posts = len(response_posts.json()['posts'])
    amount_of_likes = get_amount_of_likes(response_posts.json()['posts'])

    response = {
        'page_name': page_name,
        'page_id': page_id,
        'amount_of_posts': amount_of_posts,
        'amount_of_followers': amount_of_followers,
        'amount_of_likes': amount_of_likes
    }
    return response
