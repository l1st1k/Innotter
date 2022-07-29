from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests
from dotenv import dotenv_values

config = dotenv_values("./.env")
# config = dotenv_values("/usr/src/app/.env")
app = FastAPI()


class StatsResponseModel(BaseModel):
    page_name: str = Field(title='Название страницы', max_length=80)
    page_id: int = Field(title='ID страницы', ge=0)
    amount_of_posts: int = Field(title='Количество постов', ge=0)
    amount_of_followers: int = Field(title='Количество подписчиков', ge=0)
    amount_of_likes: int = Field(title='Количество лайков', ge=0)


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


def request_to_django(page_id: int, user_login: str, user_pass: str) -> dict:
    cookies = get_tokens_for_cookies(user_login, user_pass)
    headers = {"Authorization": f"Bearer {cookies['access_token']}", "Content-Type": "application/json"}
    response_name = requests.get(f"http://localhost:8000/api/v1/page/{page_id}/", headers=headers, cookies=cookies)
    page_name = response_name.json()["name"]
    response_followers = requests.get(f"http://localhost:8000/api/v1/page/{page_id}/followers/", headers=headers,
                                      cookies=cookies)
    amount_of_followers = len(response_followers.json()['followers'])
    response_posts = requests.get(f"http://localhost:8000/api/v1/page/{page_id}/posts/", headers=headers,
                                  cookies=cookies)
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


@app.get("/api/v1/page/{page_id}/stats", response_model=StatsResponseModel, name='Page stats by ID')
async def stats(page_id: int):
    login = 'root'
    password = 'z26p11s02'
    return request_to_django(page_id, login, password)


@app.get("/test")
async def test():
    """
    works correctly
    """
    page_id = 5
    cookies = get_tokens_for_cookies("root", "z26p11s02")
    headers = {"Authorization": f"Bearer {cookies['access_token']}", "Content-Type": "application/json"}
    response = requests.get(f"http://localhost:8000/api/v1/page/{page_id}/posts/", headers=headers, cookies=cookies)
    a = len(response.json()['posts'])
    print (a, type(a))
    return response.json()
