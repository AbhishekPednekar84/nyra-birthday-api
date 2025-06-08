import os
import dotenv
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, Header, status

dotenv.load_dotenv()

import jwt
print(jwt.__file__)

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def create_jwt_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=30)
) -> str:
    now = datetime.utcnow()
    to_encode = data.copy()
    expire = now + expires_delta

    to_encode.update({"exp": expire, "iat": now})

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def verify_jwt_token(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid auth header")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("scope") != "invitee":
            raise HTTPException(status_code=403, detail="Invalid token scope")

        return payload["sub"]

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
