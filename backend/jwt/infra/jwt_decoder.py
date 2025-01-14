from jwt.domain.jwt_decoder import IAbstractJWTDecoder
from jose import jwt, JWTError


class JWTDecoder(IAbstractJWTDecoder):
	def decode(
		self,
		token: str,
		secret_key: str,
		algorithm: str,
	) -> dict | None :
		try:
			return jwt.decode(token, secret_key, algorithms=[algorithm])
		except JWTError as e:
			print("JWT decode error", str(e))
			return None

