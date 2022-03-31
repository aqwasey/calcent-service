from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import Optional
from bson.json_util import dumps
from bson.son import SON
import json
from pydantic import BaseModel
from app.config.db import db
from app.utils.misc import from_date, to_date


@dataclass
class Amendment():
    idno: str
    policy_no: str
    old_depend: dict()
    new_depend: dict()
    entry_by: dict()  # Call center agent info
    created_on: Optional[datetime] = datetime.now()


class AmendmentModel():

    table = 'amendments'

    def __init__(self):
        self.db = db()
        self.amends = self.db[self.table]

    def add(self, amd: Amendment):
        # Insert the new record and return the results
        # it must return True (success) or False (fail)
        res = self.amends.insert_one(amd.__dict__).acknowledged
        if res:
            return 1
        return 0

    def exist(self, search: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        res = self.amends.count_documents({'policy_no': search})
        return res

    def exist(self, field: str, search: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        res = self.amends.count_documents({field: search})
        return res

    def today_by(self, agent: dict):
        # Get all records and return the results
        # it must return json empty parentheses means all or *
        res = self.amends.find(
            {"$and": [
                {"created_on": {"$gte": from_date, "$lte": to_date}}, {
                    "entry_by": SON(agent)}
            ]})
        raw = json.loads(dumps(list(res)))
        return raw

    def all_by(self, agent: dict):
        # Get all records and return the results
        # it must return json empty parentheses means all or *
        res = self.amends.find({'entry_by': SON(agent)})
        raw = json.loads(dumps(list(res)))
        return raw

    def similar(self, policy, idno):
        # Get all records and return the results
        # it must return json empty parentheses means all or *
        res = self.amends.find({"$and": [
            {"created_on": {"$gte": from_date, "$lte": to_date}}, {
                "policy_no": policy, "idno": idno}
        ]})
        raw = json.loads(dumps(list(res)))
        return raw
