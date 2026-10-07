import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
import models

# In production, set JWT_SECRET as an environment variable on Render
# (Settings -> Environment -> Add Environment Variable).
SECRET_KEY = os.environ.get("JWT_SECRET", "thiranpathai-dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # token stays valid for 7 days

# auto_error=False so routes can accept an OPTIONAL logged-in user (see get_current_user_optional)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)


def hash_password(password: str) -> str:
    # bcrypt has a 72-byte input limit — truncate defensively so long passwords don't error out
    pw_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password.encode("utf-8")[:72]
    try:
        return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _decode_user_id(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except Exception:
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """Use this when a route REQUIRES login — raises 401 if not logged in."""
    if not token:
        raise HTTPException(status_code=401, detail="Please log in to continue.")
    user_id = _decode_user_id(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Your session has expired. Please log in again.")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Account not found.")
    return user


def get_current_user_optional(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[models.User]:
    """Use this when a route works for everyone, but behaves a bit better for logged-in users."""
    if not token:
        return None
    user_id = _decode_user_id(token)
    if user_id is None:
        return None
    return db.query(models.User).filter(models.User.id == user_id).first()
