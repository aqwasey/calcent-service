from fastapi import APIRouter, Depends
from app.audit.audits_controller import AuditLogsController
from app.audit.audits_model import AuditLog
from app.registration.registration_model import Member
from app.utils.auth import AuthHandler
from app.utils.entity import AgentParam, LogParam

audit_route = APIRouter(
    prefix='/logs', tags=['logs'], dependencies=[Depends(AuthHandler().signed)])
cot = AuditLogsController()


@audit_route.post('/')
async def new_log(log: LogParam):
    if not log.info:
        return {'data': 'Provide the agent info to complete task.'}
    if not log.logs:
        return {'data': 'Provide log details to complete task.'}
    actual = AuditLog(log.info, log.logs)
    data = cot.write(actual)
    return {'data': data}


# Later check the request to GET to the token could be retrieved from the AUTH
@audit_route.post('/all')
async def overall_logs(agn: dict):
    if not agn['token']:
        return {'data': 'Provide an agent token info to complete task.'}
    data = cot.show_overall(agn)
    return {'data': data}


# Later check the request to GET to the token could be retrieved from the AUTH
@audit_route.get('/today')
async def today_logs(agn: dict):
    if not agn['token']:
        return {'data': 'Provide an agent token info to complete task.'}
    data = cot.show_today(agn)
    return {'data': data}
