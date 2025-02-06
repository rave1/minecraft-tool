from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
import jwt
from settings import SECRET_KEY


class AuthHandler:
    """
    Class housing methods for handling bearer token.
    """

    security = HTTPBearer(auto_error=False)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM = "HS256"

    def get_password_hash(self, password: str) -> str:
        """
        Function returns hashed password
        :param password: password to hash
        :return str: hashed password
        """
        return self.pwd_context.hash(secret=password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Functions verifies inputed plain text password against hashing algorithm of choice,
        in this instance it's bcrypt
        :param plain_password:
        :param hashed_password:
        :return bool:
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.exceptions.DecodeError as e:
            return e
        except Exception:
            raise RequiresLoginException()

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        if not auth:
            raise RequiresLoginException()
        return self.decode_token(auth.credentials)


class RequiresLoginException(Exception):
    pass
