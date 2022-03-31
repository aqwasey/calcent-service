from dataclasses import dataclass
from datetime import date, datetime
import json
from typing import Optional
from app.config.db import db
from bson.json_util import dumps
from bson.son import SON
from app.utils.misc import from_date, to_date


@dataclass
class Member:
    idno: str
    firstname: str
    lastname: str
    gender: str
    birth_date: str
    mobile: str
    address: str
    product: str
    regis_by: dict
    email: Optional[str] = None
    created_on: Optional[datetime] = datetime.now()


class RegistrationModel:

    table = 'registrations'

    def __init__(self):
        self.db = db()
        self.members = self.db[self.table]

    def add(self, mem: Member):
        # Insert the new record and return the results
        # it must return True (success) or False (fail)
        res = self.members.insert_one(mem.__dict__).acknowledged
        if res:
            return 1
        return 0

    def exist(self, search: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        res = self.members.count_documents({'idno': search})
        return res

    def exist(self, mobile: str, idno: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        # res = self.members.count_documents({field: search})
        res = self.members.count_documents({"mobile": mobile, "idno": idno})
        return res

    def all(self, agent: dict):
        # Get all records and return the results
        # it must return json
        # empty parentheses means all or *
        res = self.members.find({"regis_by": SON(agent)})
        return json.loads(dumps(list(res)))

    def today(self, agent: dict):
        # Get all records and return the results
        # it must return json
        # empty parentheses means all or *
        #res = self.members.find({})
        res = self.members.find({
            "$and": [{
                "created_on": {'$gte': from_date, "$lte": to_date}},
                {"regis_by": SON(agent)}]})
        return json.loads(dumps(list(res)))
