from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator

class Status(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

def validate_phone(value):
    if not (value.isdigit() and len(value) == 10 and value.startswith("0")):
        raise ValueError("must be 10 digits starting with 0, e.g. 0245567812")
    return value

class ApplicationBase(BaseModel):
    fullName: str = Field(min_length=3, max_length=100)
    email: EmailStr
    phone: str
    whatsappNumber: str
    university: str = Field(min_length=2)
    course: str = Field(min_length=2)
    level: str
    track: str
    motivation: str = Field(min_length=20, max_length=1000)
    portfolioLink: Optional[HttpUrl] = None
    resumeLink: Optional[HttpUrl] = None
    joinInnovationClub: bool = False

    @field_validator("phone", "whatsappNumber")
    @classmethod
    def check_phone(cls, value):
        return validate_phone(value)


class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int
    status: Status
    submittedAt: datetime

class ApplicationUpdate(BaseModel):
    fullName: Optional[str] = Field(default=None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsappNumber: Optional[str] = None
    university: Optional[str] = Field(default=None, min_length=2)
    course: Optional[str] = Field(default=None, min_length=2)
    level: Optional[str] = None
    track: Optional[str] = None
    motivation: Optional[str] = Field(default=None, min_length=20, max_length=1000)
    portfolioLink: Optional[HttpUrl] = None
    resumeLink: Optional[HttpUrl] = None
    joinInnovationClub: Optional[bool] = None
    status: Optional[Status] = None

    @field_validator("phone", "whatsappNumber")
    @classmethod
    def check_phone(cls, value):
        if value is None:
            return value
        return validate_phone(value)
