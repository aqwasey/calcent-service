
from app.registration.registration_model import Member, RegistrationModel


class RegistrationController:

    def __init__(self):
        self.mod = RegistrationModel()

    def save(self, mem: Member):
        # Check if item already exist else create it
        check_info = self.mod.exist(mem.mobile, mem.idno)
        print(check_info)
        if check_info >= 1:
            return 'Member record already exist or already created.'
        # Create a new item
        result = self.mod.add(mem)
        if result >= 1:
            return 'Member registered successfully!'
        return 'Error:- registering new member, try again'

    def today_registrations(self, agent: dict()):
        # select all the items using no filter
        result = self.mod.today(agent)
        if len(result) > 0:
            return result
        return 'No new registration(s) recorded today by this agent.'

    def overall_registrations(self, agent_info: dict()):
        # select all the items using agent info as a filter
        result = self.mod.all(agent_info)
        if len(result) > 0:
            return result
        return 'No overall new registration records are associated with this agent.'

    def agent_signups_records(self, agent_info: dict()):
        # select all the items using no filter
        result = self.mod.all_by(agent_info)
        if len(result) > 0:
            return result
        return 'No membership records are were found.'
