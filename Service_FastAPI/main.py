from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests
from dotenv import dotenv_values

config = dotenv_values("/usr/src/app/.env")
app = FastAPI()


class StatsResponseModel(BaseModel):
    page_name: str = Field(title='Название страницы', max_length=80)
    page_id: int = Field(title='ID страницы', ge=0)
    amount_of_posts: int = Field(title='Количество постов', ge=0)
    amount_of_followers: int = Field(title='Количество подписчиков', ge=0)
    amount_of_likes: int = Field(title='Количество лайков', ge=0)


def request_to_django(page_id, access_token=False) -> StatsResponseModel:
    access_token = "xz"
    headers = {"Authorization": f"Bearer {access_token}", "accept": "application/json"}
    response_followers = requests.get(f"http://localhost:8000/api/v1/page/{page_id}/followers/", headers=headers)
    response_posts = requests.get(f"http://localhost:8000/api/v1/page/{page_id}/posts/", headers=headers)
    response = StatsResponseModel()
    return response


@app.get("/api/v1/page/{page_id}/stats")
async def stats(page_id: int) -> StatsResponseModel:
    return request_to_django(page_id)
