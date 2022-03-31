import re
from app.complains.complains_model import ComplainsModel, Complains
from app.utils.entity import ComplainsParam


class ComplainsController:

    def __init__(self):
        self.mod = ComplainsModel()

    def save(self, com: ComplainsParam):
        # Check if item already exist else create it
        check_info = self.mod.exist_info(com.info)
        check_crn = self.mod.exist('crn', com.crn)
        if check_info >= 1:
            return 'Complain record already exist or already created.'
        if check_crn >= 1:
            return 'Complain reference number already exist'
        # Create a new item
        new_com = Complains(related=com.related, specific=com.specific, 
                        msg=com.msg, info=com.info, entry_by=com.entry_by, crn=com.crn)
        result = self.mod.add(new_com)
        if result >= 1:
            return 'Complain Query registered successfully!'
        return 'Error:- registering a complain query, try again'

    def show_today(self, agent: dict):
        # select all the items using no filter
        result = self.mod.today(agent)
        if len(result) > 0:
            return result
        return 'No caller query recorded today by this agent.'

    def show_all(self, agent: dict):
        # select all the items using no filter
        result = self.mod.all(agent)
        if len(result) > 0:
            return result
        return 'No overall complaint query records are associated with this agent.'

    def show_related(self, cate: str, agent_info: dict):
        # select all the items using the filter (category & agent info)
        result = self.mod.related(cate, agent_info)
        if len(result) > 0:
            return result
        return 'No related complaint query records were found with this agent and category item.'
