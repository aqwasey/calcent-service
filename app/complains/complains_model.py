from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime
import json
from bson.json_util import dumps
from bson.son import SON
from app.config.db import db
from app.utils.misc import from_date, to_date
from app.utils.pkeys import RussianRoullete as rr

@dataclass
class Complains:
    related: str
    specific: str
    msg: str
    info: list
    entry_by: dict
    crn: Optional[str] = rr.complain_code()
    created_on: Optional[datetime] = datetime.now()


class ComplainsModel:

    table = 'complains'

    def __init__(self):
        self.db = db()
        self.complains = self.db[self.table]

    def add(self, com: Complains):
        # Insert the new record and return the results
        # it must return True (success) or False (fail)
        res = self.complains.insert_one(com.__dict__).acknowledged
        if res:
            return 1
        return 0

    def exist_info(self, item: list):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        res = self.complains.count_documents({'info': {'$all': item }})
        return res
    
    def exist(self, field: str, search: str):
        # Check if record exist and return the count number
        # it must return a positive number or 0 if doesn't exist
        res = self.complains.count_documents({field: search})
        return res

    def today(self, agent: dict):
        # Get all records and return the results
        # it must return json
        # empty parentheses means all or *
        res = self.complains.find({
            "$and": [{
                "created_on": {'$gte': from_date, "$lte": to_date}},
                {"entry_by": SON(agent)}]})
        return json.loads(dumps(list(res)))

    def all(self, agent: dict):
        # Get all records and return the results
        # it must return json
        # empty parentheses means all or *
        res = self.complains.find({'entry_by': SON(agent)})
        return json.loads(dumps(list(res)))

    def related(self, category: str, agent: dict):
        # Check if category item has been referenced or linked
        # to any existing product
        res = self.complains.find(
            {'related': category, "entry_by": SON(agent)})
        return json.loads(dumps(list(res)))

    def specific_items(self, specific: str, agent: dict):
        # Check if category item has been referenced or linked
        # to any existing product
        res = self.complains.find(
            {'specific': specific, "entry_by": SON(agent)})
        return json.loads(dumps(list(res)))
