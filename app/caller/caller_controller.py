
from app.caller.caller_model import Caller, CallerModel


class CallersController:

    def __init__(self):
        self.mod = CallerModel()

    def save(self, call: Caller):
        # Check if item already exist else create it
        check_info = self.mod.exist('phone_no', call.phone_no)
        if check_info >= 1:
            return 'Caller record already exist or already created.'
        # Create a new item
        result = self.mod.add(call)
        if result >= 1:
            return 'Caller Query registered successfully!'
        return 'Error:- registering caller query, try again'

    def show_today(self, agent: dict):
        # select all the items using no filter
        result = self.mod.count_agent_today(agent)
        if len(result) > 0:
            return result
        return 'No caller query recorded today by this agent.'

    def show_overall(self, agent_info: dict):
        # select all the items using no filter
        result = self.mod.count_agent_all(agent_info)
        if len(result) > 0:
            return result
        return 'No caller query records are overall associated with this agent.'


    def show_related(self, cate: str, agent_info: dict):
        # select all the items using the filter (category & agent info)
        result = self.mod.related_callers(cate, agent_info)
        if len(result) > 0:
            return result
        return 'No related caller query records were found with this agent and category item.'
