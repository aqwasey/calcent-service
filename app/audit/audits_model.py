from dataclasses import dataclass
from datetime import date, datetime
import json
from typing import Optional
from bson.son import SON
from app.config.db import db
from bson.json_util import dumps
from app.utils.misc import from_date, to_date


@dataclass
class AuditLog:
    user_info: dict()
    logs: dict()
    created_on: Optional[datetime] = datetime.now()


class AuditLogsModel:

    table = 'auditlogs'

    def __init__(self):
        self.db = db()
        self.audits = self.db[self.table]

    def add(self, aud: AuditLog):
        # Insert the new record and return the results
        # it must return True (success) or False (fail)
        res = self.audits.insert_one(aud.__dict__).acknowledged
        if res:
            return 1
        return 0

    def overall_logs(self, agent: dict):
        # Get all records and return the results
        # it must return json
        # empty parentheses means all or *
        raw = self.audits.find({"user_info": SON(agent)})
        return json.loads(dumps(list(raw)))

    def today_logs(self, agent: dict):
        # Get all records and return the results
        # it must return json
        raw = self.audits.find({
            "$and": [{
                "created_on": {'$gte': from_date, "$lte": to_date}},
                {"user_info": SON(agent)}]})
        return json.loads(dumps(list(raw)))
