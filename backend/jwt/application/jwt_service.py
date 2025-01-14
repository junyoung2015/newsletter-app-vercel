from jwt.infra.jwt_encoder import JWTEncoder
from jwt.infra.jwt_decoder import JWTDecoder
from datetime import datetime
from zoneinfo import ZoneInfo

class JWTService:
	"""
	JWT 로그인시 access token 생성 및 refresh token 생성
	"""
	def __init__(
		self,
		encoder: JWTEncoder,
		decoder: JWTDecoder,
		algorithms: str = None,
		secret_key: str = None,
		access_token_expire_time: int = None,
		refresh_token_expire_time: int = None,
	):
		self.encoder = encoder
		self.decoder = decoder
		self.algorithms = algorithms
		self.secret_key = secret_key
		self.access_token_expire_time = access_token_expire_time
		self.refresh_token_expire_time = refresh_token_expire_time

	def create_access_token(self, payload: dict) -> str:
		"""
		access token 생성
		"""
		return self._create_token(payload, self.access_token_expire_time)

	def create_refresh_token(self, payload: dict) -> str:
		"""
		refresh token 생성
		"""
		return self._create_token(payload, self.refresh_token_expire_time)

	def _create_token(self, payload: dict, expire_delta: int) -> str:
		"""
		token 생성
		"""
		return self.encoder.encode(
			payload=payload,
			expires_delta=expire_delta,
			secret_key=self.secret_key,
			algorithms=self.algorithms
		)

	def check_token_expire(self, token: str) -> dict | None:
		"""
		token 만료 확인
		"""
		payload = self.decoder.decode(token, self.secret_key, self.algorithms)
		now = datetime.timestamp(datetime.now(ZoneInfo("Asia/Seoul")))
		if payload and payload["exp"] < now:
			return None
		return payload
