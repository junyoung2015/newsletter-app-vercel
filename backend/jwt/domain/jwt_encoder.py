from abc import ABCMeta, abstractmethod

class IAbstractJWTEncoder(metaclass=ABCMeta):
	"""
	JWT 인코더 추상 클래스
	encode 메소드 구현

	:param payload: JWT에 담을 데이터
	:param expires_delta: 만료 시간
	:param secret_key: JWT 암호화 키
	:param algorithms: JWT 암호화 알고리즘

	"""
	@abstractmethod
	def encode(
		self,
		payload: dict,
		expires_delta: int,
		secret_key: str,
		algorithms: str,
	) -> str:
		pass

