from jwt.application.jwt_service import JWTService
from jwt.infra.jwt_decoder import JWTDecoder
from jwt.infra.jwt_encoder import JWTEncoder
from user.domain.user import User
from fastapi import HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from config import get_settings
from enum import StrEnum
from dataclasses import dataclass
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

# 환경변수
settings = get_settings()
SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_time
REFRESH_TOKEN_EXPIRE_TIME = settings.refresh_token_expire_time

print(ALGORITHM)
class Role(StrEnum):
	ADMIN = "ADMIN"
	USER = "USER"

@dataclass
class CurrentUser:
	id: str
	role: Role

jwt_service = JWTService(
	encoder=JWTEncoder(),
	decoder=JWTDecoder(),
	secret_key=SECRET_KEY,
	algorithms=ALGORITHM,
	access_token_expire_time=ACCESS_TOKEN_EXPIRE_TIME,
	refresh_token_expire_time=REFRESH_TOKEN_EXPIRE_TIME
)

async def validate_token(request: Request) -> str | None:
	authorization = request.headers.get("Authorization")
	schema, param = get_authorization_scheme_param(authorization)
	if not authorization or schema.lower() != "bearer":
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token is invalid",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return param

def get_current_user(token: Annotated[str, Depends(validate_token)]):
	try:
		validate_payload = jwt_service.check_token_expire(token)
		if validate_payload:
			user_id = validate_payload.get("user_id")
			role = validate_payload.get("role")
		else:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token is invalid",
				headers={"WWW-Authenticate": "Bearer"},
			)
	except HTTPException as e:
		raise e
	else:
		if not user_id or not role or role != Role.USER:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="User not found",
				headers={"WWW-Authenticate": "Bearer"},
			)
		else:
			return CurrentUser(user_id, role)

#TODO: admin 유저 아이디 세팅하기
def get_admin_user(token: Annotated[str, Depends(validate_token)]):
	try:
		validate_payload = jwt_service.check_token_expire(token)
		if validate_payload:
			role = validate_payload.get("role")
		else:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token is invalid",
				headers={"WWW-Authenticate": "Bearer"},
			)
	except HTTPException as e:
		raise e
	else:
		if not role or role != Role.ADMIN:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="User is not an administrator",
				headers={"WWW-Authenticate": "Bearer"},
			)
		else:
			return CurrentUser("ADMIN_USER_ID", role)
