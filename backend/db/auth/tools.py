from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Functions verifies inputed plain text password against hashing algorithm of choice,
    in this instance it's bcrypt
    :param plain_password:
    :param hashed_password:
    :return bool:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Function returns hashed password
    :param password: password to hash
    :return str: hashed password
    """
    return pwd_context.hash(secret=password)


def auth_user(hashed_password: str) -> bool:
    pass
