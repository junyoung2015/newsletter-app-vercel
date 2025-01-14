from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, EmailStr
from dependency_injector.wiring import inject, Provide
from user.application.user_service import UserService
from containers import Container
from datetime import datetime
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from common.auth import CurrentUser, get_current_user
from news.application.news_service import NewsService
from jwt.application.jwt_service import JWTService
from fastapi.responses import JSONResponse
from  fastapi import status

router = APIRouter(prefix="/api/user")

class UserBody(BaseModel):
	username: EmailStr = Field(max_length=64)
	password: str = Field(min_length=8, max_length=64)

class UserResponse(BaseModel):
	id: str
	email: str

class NewsItem(BaseModel):
	name: str
	description: str
	send_frequency: str

class NewsResponse(BaseModel):
	news: List[NewsItem]

class LoginResponse(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = "bearer"

@router.post("/register", status_code=201, response_model=UserResponse)
@inject
async def create_user(
	user: UserBody,
	user_service: UserService = Depends(Provide[Container.user_service])
):
	created_user = await user_service.create_user(
		email=user.username,
		password=user.password,
	)
	return created_user

@router.post("/login", response_model=LoginResponse)
@inject
async def login(
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
	user_service: UserService = Depends(Provide[Container.user_service]),
	jwt_service: JWTService = Depends(Provide[Container.jwt_service])
):
	jwt: dict = await user_service.login(
		email=form_data.username,
		password=form_data.password,
		jwt_service=jwt_service,
	)
	response = JSONResponse(content={"messages": "login successful"}, status_code=status.HTTP_200_OK)
	response.set_cookie(
		key="access_token",
		value=jwt["access_token"],
		httponly=True,
		secure=False, # HTTPS
		samesite="lax", # 벡엔드와 프론트엔드가 분리된 환경에서는 none으로 세팅
		domain="localhost", #TODO: 도메인 사야함
	)
	response.set_cookie(
		key="refresh_token",
		value=jwt["refresh_token"],
		httponly=True,
		secure=False, # HTTPS
		samesite="lax", # 벡엔드와 프론트엔드가 분리된 환경에서는 none으로 세팅
		domain="localhost", #TODO: 도메인 사야함
	)
	return response

@router.get("/news", response_model=NewsResponse)
@inject
async def get_news(
	current_user: Annotated[CurrentUser, Depends(get_current_user)],
	news_service: NewsService = Depends(Provide[Container.news_service])
):
	news = await news_service.get_news(current_user.id)
	reduced_news = [NewsItem(name=n.name, description=n.description, send_frequency=n.send_frequency) for n in news]
	return {"news": reduced_news}

@router.get("/me", status_code=200, response_model=UserResponse)
@inject
async def get_user_me(
	current_user: Annotated[CurrentUser, Depends(get_current_user)],
	user_service: UserService = Depends(Provide[Container.user_service])
):
	user = await user_service.get_user_by_id(current_user.id)
	print(user)
	return user
