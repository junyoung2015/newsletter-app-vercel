from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import List
from dependency_injector.wiring import inject, Provide
from typing import Annotated
from common.auth import CurrentUser, get_current_user
from news.application.news_service import NewsService
from containers import Container
from fastapi.responses import JSONResponse
from common.celery import app
from celery.result import AsyncResult

router = APIRouter(prefix="/api/news")


class NewsBody(BaseModel):
    name: str = Field(..., max_length=256)
    description: str
    custom_prompt: str = Field(None)
    send_frequency: str = Field(
        ...,
        pattern="^(daily|weekly|monthly|bi-weekly)$",
        description="발송 빈도 (daily, weekly, monthly 중 하나)",
    )
    is_active: bool = Field(default=True)
    topic: List[str] = Field(..., description="뉴스레터 토픽 리스트")
    source: List[str] = Field(..., description="뉴스레터 url 리스트")


class CreateNewsletterTaskBody(BaseModel):
    topics: List[str] = Field(..., description="뉴스레터 토픽 리스트")
    sources: List[str] = Field(..., description="뉴스레터 url 리스트")


class CreateNewsletterBody(BaseModel):
    newsletter_id: int


class NewsletterSentResponse(BaseModel):
    name: str
    generated_content: str


@router.post("/save", status_code=201)
@inject
async def save_news(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: NewsBody,
    news_service: NewsService = Depends(Provide[Container.news_service]),
):
    newsletter_id = await news_service.save_news(
        user_id=current_user.id,
        name=body.name,
        description=body.description,
        custom_prompt=body.custom_prompt,
        send_frequency=body.send_frequency,
        is_active=body.is_active,
        topic=body.topic if body.topic else [],
        source=body.source if body.source else [],
    )
    response = JSONResponse(content={"newsletter_id": newsletter_id}, status_code=201)
    return response


@router.post("/task", status_code=201)
@inject
def create_newsletter_task(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: CreateNewsletterTaskBody,
    news_service: NewsService = Depends(Provide[Container.news_service]),
):
    task = news_service.create_newsletter_task(
        topics=body.topics,
        sources=body.sources,
    )
    response = JSONResponse(content={"task_id": task.id}, status_code=201)
    return response


# 보낸 뉴스레터 저장하지 않고 조회만 할 때
@router.get("/example/{task_id}")
@inject
def get_newsletter(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    task_id: str,
):
    task: AsyncResult = app.AsyncResult(task_id)
    if task.ready():
        response: NewsletterSentResponse = task.get()
        return response
    else:
        response = JSONResponse(
            content={"status": "pending"}, status_code=200
        )  # 뉴스레터 생성 중
        return response


# 보낸 뉴스레터 저장할 때
@router.post("/create/{task_id}", status_code=201)
@inject
async def create_newsletter_sent(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    task_id: str,
    body: CreateNewsletterBody,
    news_service: NewsService = Depends(Provide[Container.news_service]),
):
    task: AsyncResult = app.AsyncResult(task_id)
    if task.ready():
        response: NewsletterSentResponse = await news_service.save_sent_newsletter(
            newsletter_id=body.newsletter_id,
            newsletter_sent_result=task.get(),
        )
        return response
    else:
        response = JSONResponse(
            content={"status": "pending"}, status_code=200
        )  # 뉴스레터 생성 중
        return response
