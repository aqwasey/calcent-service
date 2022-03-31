from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from bson.json_util import dumps
from app.utils.entity import AgentParam
from app.config.db import db
import json
from bson.son import SON
from app.utils.misc import from_date, to_date


@dataclass
class Caller:
    fullname: str
    gender: str
    phone_no: str
    category: str
    location: str
    action: str
    priority: int
    entry_by: dict
    created_on: Optional[datetime] = datetime.today()


class CallerModel:

    table = 'callers_register'

    def __init__(self):
        self.db = db()
        self.caller = self.db[self.table]

    def add(self, cal: Caller):
        # Insert the new record and return the results
        # it must return True (success) or False (fail)
        res = self.caller.insert_one(cal.__dict__).acknowledged
        if res:
            return 1
        return 0

    def exist(self, field: str, search: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        res = self.caller.count_documents({field: search})
        return res

    def count_agent_today(self, agent: dict):
        raw = self.caller.find({
            "$and": [{
                "created_on": {'$gte': from_date, "$lte": to_date}},
                {"entry_by": SON(agent)}]})
        return json.loads(dumps(list(raw)))

    def count_agent_all(self, agent: dict):
        raw = self.caller.find({"entry_by": SON(agent)})
        return json.loads(dumps(list(raw)))

    def related_callers(self, category_item: str, agent: dict):
        # Check if category item has been referenced or linked
        # to any existing product
        res = self.caller.find(
            {'category': category_item, 'entry_by': SON(agent)})
        return json.loads(dumps(list(res)))
