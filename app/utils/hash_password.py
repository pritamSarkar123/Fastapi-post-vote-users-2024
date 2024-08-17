from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_plain_text_password(password: str):
    return pwd_context.hash(password)


def verify(password_string, password_hashed):
    return pwd_context.verify(password_string, password_hashed)
