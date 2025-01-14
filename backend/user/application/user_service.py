from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from dependency_injector.wiring import inject
from fastapi import HTTPException, status
from utils.crypto import Crypto
from common.auth import Role
from jwt.application.jwt_service import JWTService

#TODO: 비밀번호 변경, 회원탈퇴 등
class UserService:
	@inject
	def __init__(
		self,
		user_repo: IUserRepository,
	):
		self.user_repo = user_repo
		self.ulid = ULID()
		self.crypto = Crypto()

	async def create_user(
		self,
		email: str,
		password: str,
	):
		_user = None
		try:
			_user = await self.user_repo.find_by_email(email)
		except HTTPException as e:
			if e.status_code != 422:
				raise e
		if _user:
			raise HTTPException(status_code=422, detail="User already exists")

		now = datetime.now()
		user: User = User(
			id=self.ulid.generate(),
			email=email,
			password_hash=self.crypto.encrypt(password),
			created_at=now,
			updated_at=now,
		)
		await self.user_repo.save(user)
		return user


	async def login(self, email: str, password: str, jwt_service: JWTService):
		user: User = await self.user_repo.find_by_email(email)
		if not self.crypto.verify(password, user.password_hash):
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

		payload = {
			"user_id": user.id,
			"role": Role.USER,
		}

		access_token = jwt_service.create_access_token(payload=payload)
		refresh_token = jwt_service.create_refresh_token(payload=payload)
		return {
			"access_token": access_token,
			"refresh_token": refresh_token
		}

	async def get_user_by_id(self, user_id: str):
		return await self.user_repo.find_by_id(user_id)


