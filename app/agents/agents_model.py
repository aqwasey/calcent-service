from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from pydantic import EmailStr
from app.config.db import db
from app.utils.pkeys import RussianRoullete as rr
from app.utils.auth import AuthHandler as aut
from bson.json_util import dumps
import json


@dataclass
class Agent:
    othername: str
    surname: str
    gender: str
    birthdate: str
    idnumber: str
    mobile: str
    email: EmailStr
    password: str
    address: Optional[str] = None
    department: Optional[str] = None
    photo: Optional[str] = None
    access_pin: Optional[str] = rr.access_pin()
    status: Optional[str] = 'Active'
    created_on: Optional[datetime] = datetime.today()


class AgentsModel:

    table = "agents"

    def __init__(self):
        self.db = db()
        self.agents = self.db[self.table]

    def add(self, agn: Agent):
        # Insert the new record and return the results
        # it must return True (success) or False (fail)
        res = self.agents.insert_one(agn.__dict__).acknowledged
        if res:
            return 1
        return 0

    def exist(self, field: str, search: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        res = self.agents.count_documents({field: search})
        return res

    def getIn(self, username: EmailStr, password: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        raw = self.agents.find({'email': username, 'password': password}, {
                               'email': 1, 'access_pin': 1, 'othername': 1, 'surname': 1})
        return json.loads(dumps(list(raw)))

    def getPwd(self, username):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        raw = self.agents.find({'email': username}, {
                               '_id': 0, 'password': 1, 'access_pin': 1, 'othername': 1, 'surname': 1})
        return json.loads(dumps(list(raw)))

    def getProfile(self, username: EmailStr, pin: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        raw = self.agents.find(
            {'email': username, 'access_pin': pin}, {'_id': 0})
        return json.loads(dumps(list(raw)))
