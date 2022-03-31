from pprint import pprint
from bson.json_util import dumps
from app.agents.agents_model import Agent, AgentsModel
from app.utils.auth import AuthHandler
import json


class AgentsController:

    aut = AuthHandler()

    def __init__(self):
        self.mod = AgentsModel()

    def save(self, agent: Agent):
        # Check if email already exist in the database
        email_exist = self.mod.exist('email', agent.email)
        if email_exist > 0:
            return "Email provided already exist or duplicate not allowed"
        email_idno = self.mod.exist('idnumber', agent.idnumber)
        if email_idno > 0:
            return "ID Number provided already exist or duplicate not allowed"
        email_mob = self.mod.exist('mobile', agent.mobile)
        if email_mob > 0:
            return "Mobile or Cellphone number already exist or duplicate not allowed"
        res = self.mod.add(agent)
        if res >= 1:
            return 'Agent Profile registered successfully!'
        return 'Error:- registering agent profile query, try again'

    def login(self, username: str, password: str):
        username_exist = self.mod.exist('email', username)
        if username_exist == 0:
            return "Agent login account does not exist"
        data = self.mod.getPwd(username)
        hash_password = data[0]['password']
        if not self.aut.verify_pwd(password, hash_password):
            return "Agent login credentials does not exist or invalid"
        token = self.aut.tokenize(username, data[0]['access_pin'],
                                  str(data[0]['othername'] + ' ' + data[0]['surname']))
        return token
