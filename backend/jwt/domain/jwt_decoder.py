from abc import ABCMeta, abstractmethod

class IAbstractJWTDecoder(metaclass=ABCMeta):
	"""
	JWT 디코더 추상 클래스
	decode 메소드 구현

	:param token: JWT 토큰
	:param secret_key: JWT 암호화 키
	:param algorithms: JWT 암호화 알고리즘
	"""
	@abstractmethod
	def decode(
		self,
		token: str,
		secret_key: str,
		algorithms: str,
	) -> dict | None:
		pass
