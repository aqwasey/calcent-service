from app.amendment.amendments_model import AmendmentModel, Amendment
from app.utils.entity import AmendmentParam
from fastapi import BackgroundTasks, HTTPException


class AmendmentsController():

    def __init__(self):
        self.mod = AmendmentModel()

    def save(self, aud: Amendment):
        # Check if record already exist
        check_by_policy = self.mod.exist('policy_no', aud.policy_no)
        check_by_idnumber = self.mod.exist('idno', aud.idno)
        if check_by_policy:
            return 'An Amendment entry has been made with the same POLICY Number'
        if check_by_idnumber:
            return 'An Amendment entry has been made with the same ID Number'
        result = self.mod.add(aud)
        if result == 1:
            return 'Amendment entry made successfully!'

    def show_today(self, info: dict):
        # select all the items using no filter
        result = self.mod.today_by(info)
        if len(result) > 0:
            return result
        return 'No Amendment records(s) found today.'

    def show_overall(self, info: dict):
        # select all the items using no filter
        result = self.mod.all_by(info)
        if len(result) > 0:
            return result
        return 'No overall amendments records(s) found.'

    def show_similar(self, polno: str, idno: str):
        # Check and retrieve records of a similar entry
        # using the policy and id number parameters
        result = self.mod.similar(polno, idno)
        if len(result) > 0:
            return result
        return 'No similar amendment record was found with the provided Policy or ID Number.'
