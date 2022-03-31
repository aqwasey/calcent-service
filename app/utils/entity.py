from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from bson.json_util import dumps
from app.utils.pkeys import RussianRoullete as rr


class LogParam(BaseModel):
    info: dict
    logs: dict
    created_on: Optional[datetime] = datetime.now()


class AgentParam(BaseModel):
    token: str
    fullname: str


class AgentUser(BaseModel):
    othername: str
    surname: str
    gender: str
    birthdate: str
    idnumber: str
    mobile: str
    email: EmailStr
    password: str


class AmendmentParam(BaseModel):
    idnum: str
    policy: str
    old_info: dict
    new_info: dict
    created_on: Optional[datetime] = datetime.now()


class CallerParam(BaseModel):
    fullname: str
    gender: str
    phone_no: str
    category: str
    location: str
    action: str
    priority: int
    entry_by: Optional[dict] = None
    created_on: Optional[datetime] = datetime.today()


class ComplainsParam(BaseModel):
    related: str
    specific: str
    msg: str
    info: list
    entry_by: Optional[dict] = None
    crn: Optional[str] = rr.complain_code()
    created_on: Optional[datetime] = datetime.now()


class AuthInfo(BaseModel):
    username: EmailStr
    password: str
