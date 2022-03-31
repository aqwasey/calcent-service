from fastapi import Request
from app.audit.audits_model import AuditLog
from app.utils.auth import AuthHandler


def pssh(data: str):
    return data.split(" ")[1]


def rawUser(reqs: Request):
    return AuthHandler().token_data(pssh(reqs.headers['authorization']))


def my_log(fullname, token, title, msg):
    return AuditLog(
        user_info={"fullname": fullname, "token": token},
        logs={"task": title, "action": msg})
