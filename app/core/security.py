import hashlib
import bcrypt
import jwt

from calendar import timegm
from datetime import timedelta, datetime, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError

from app.api.exceptions import CustomException
from app.core.config import SECRET_KEY, PAYMENT_SECRET

ALGORITHM = "HS256"
ACCESS_TOKEN_TTL: timedelta = timedelta(minutes=60)
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth/login_docs")


def convert_to_timestamp(datetime: datetime) -> int:
    """
    the utility converts the datetime in UNIX.
    """
    return timegm(datetime.utctimetuple())


def generate_access_token(pk) -> str:
    current_timestamp = convert_to_timestamp(datetime.now(tz=timezone.utc))
    data = {"exp": current_timestamp + int(ACCESS_TOKEN_TTL.total_seconds()), "id": pk}
    return jwt.encode(payload=data, key=SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(
    token: str = Depends(OAUTH2_SCHEME),
) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidSignatureError:
        raise CustomException(
            status_code=401,
            detail="Incorrect token signature",
            message="Incorrect token signature",
        )
    except ExpiredSignatureError:
        raise CustomException(
            status_code=401,
            detail="Token expired",
            message="Token expired",
        )
    except DecodeError:
        raise CustomException(
            status_code=401,
            detail="Unable to decode token",
            message="Incorrect token",
        )


def create_signature(payment: dict) -> str:
    sorted_payment = sorted(tuple(payment.items()), key=lambda x: x[0])
    payment_string = ''.join(str(i[1]) for i in sorted_payment) + PAYMENT_SECRET

    sha256_hash = hashlib.sha256()
    sha256_hash.update(payment_string.encode('utf-8'))

    return sha256_hash.hexdigest()


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(provided_password: str, stored_hash) -> bool:
    return bcrypt.checkpw(provided_password.encode("utf-8"), stored_hash)
