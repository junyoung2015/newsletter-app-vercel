from jwt.domain.jwt_encoder import IAbstractJWTEncoder
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import jwt

class JWTEncoder(IAbstractJWTEncoder):
	def encode(
		self,
		payload: dict,
		expires_delta: int,
		secret_key: str,
		algorithms: str
	) -> str:
		to_encode = payload.copy()
		expire = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(minutes=expires_delta)
		to_encode.update({"exp": expire})
		return jwt.encode(to_encode, secret_key, algorithm=algorithms)
