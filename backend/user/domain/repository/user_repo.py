from abc import ABCMeta, abstractmethod
from user.domain.user import User
from typing import List
from sqlalchemy import Connection

class IUserRepository(metaclass=ABCMeta):
	@abstractmethod
	async def find_by_id(self, id: str) -> User:
		"""
		유저 ID로 유저를 검색한다.
		검색한 유저가 없을 경우 422 에러를 발생시킨다.
		"""
		raise NotImplementedError

	@abstractmethod
	async def find_by_email(self, email: str) -> User:
		"""
		이메일로 유저를 검색한다.
		검색한 유저가 없을 경우 422 에러를 발생시킨다.
		"""
		raise NotImplementedError

	@abstractmethod
	async def save(self, user: User) -> None:
		"""
		유저를 DB에 저장한다.
		"""
		raise NotImplementedError

	# @abstractmethod
	# async def delete(self, user: User, conn: Connection) -> None:
	# 	"""
	# 	유저를 삭제한다.
	# 	"""
	# 	raise NotImplementedError

	# @abstractmethod
	# async def find_all(self) -> List[User]:
	# 	pass
