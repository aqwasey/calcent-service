from lib2to3.pgen2 import token
import requests as req
import json as js
from app.audit.audits_controller import AuditLogsController
from app.audit.audits_model import AuditLogsModel
from app.utils.auth import AuthHandler
from app.utils.entity import AgentParam

URL = "http://127.0.0.1:8000/"

logs_path = "logs/"
amends_path = "amendments/"
audit_path = "audits/"


def main():
    auth = AuthHandler()
    print(auth.hashit("dome"))


if __name__ == '__main__':
    # test_main()
    # test()
    main()
