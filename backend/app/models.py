from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class OAuthProvider(str, Enum):
    """OAuth provider types"""

    GOOGLE = "google"
    KAKAO = "kakao"


class ProviderType(str, Enum):
    """Provider types"""

    SOCIAL = "social"
    EMAIL = "email"


class UserBase(BaseModel):
    """Base user model"""

    email: EmailStr
    display_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    """User creation model"""

    uuid: str
    provider: OAuthProvider
    provider_type: ProviderType = ProviderType.SOCIAL
    user_status: bool = True
    created_at: datetime
    last_sign_in_at: datetime


class User(UserBase):
    """User model"""

    id: int
    uuid: str
    provider: OAuthProvider
    provider_type: ProviderType
    user_status: bool
    created_at: datetime
    last_sign_in_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """User response model"""

    uuid: str
    email: EmailStr
    display_name: Optional[str] = None
    provider: str
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    """Token model"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data model"""

    sub: str  # uuid
    email: Optional[EmailStr] = None
