from dependency_injector import containers, providers

from user.application.user_service import UserService
from news.application.news_service import NewsService
from jwt.application.jwt_service import JWTService

from user.infra.repository.user_repo import UserRepository
from news.infra.repository.news_repo import NewsRepository
from jwt.infra.jwt_decoder import JWTDecoder
from jwt.infra.jwt_encoder import JWTEncoder
from config import get_settings


settings = get_settings()
SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_time
REFRESH_TOKEN_EXPIRE_TIME = settings.refresh_token_expire_time

class Container(containers.DeclarativeContainer):
	# 의존성 관리한 패키지 추가
	wiring_config = containers.WiringConfiguration(
		packages=[
			"user",
			"news",
			"jwt",
		]
	)
	encoder = providers.Factory(JWTEncoder)
	decoder = providers.Factory(JWTDecoder)
	jwt_service = providers.Factory(
		JWTService,
		encoder=encoder,
		decoder=decoder,
		secret_key=SECRET_KEY,
		algorithms=ALGORITHM,
		access_token_expire_time=ACCESS_TOKEN_EXPIRE_TIME,
		refresh_token_expire_time=REFRESH_TOKEN_EXPIRE_TIME
	)

	news_repo = providers.Factory(NewsRepository)
	news_service = providers.Factory(NewsService, news_repo=news_repo)

	user_repo = providers.Factory(UserRepository)
	user_service = providers.Factory(UserService, user_repo=user_repo)
