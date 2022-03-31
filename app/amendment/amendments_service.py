from pprint import pprint
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from app.amendment.amendments_controller import AmendmentsController
from app.amendment.amendments_model import Amendment
from app.audit.audits_controller import AuditLogsController
from app.audit.audits_model import AuditLog
from app.utils.auth import AuthHandler
from app.utils.entity import AgentParam, AmendmentParam
from app.utils.quikie import my_log, rawUser

amend_route = APIRouter(
    prefix='/amendments', tags=['amendments'], dependencies=[Depends(AuthHandler().signed)])
opn = AmendmentsController()
elog = AuditLogsController()


@amend_route.post('/')
async def new_amendment(amn: AmendmentParam, reqs: Request, bgtask: BackgroundTasks):
    try:
        if not amn.policy:
            raise HTTPException(
                status_code=400, detail='Provide the Amendment Policy Number.')
        if not amn.idnum:
            raise HTTPException(
                status_code=400, detail='Provide Policy Holder ID number for Amendment.')
        if not amn.old_info:
            raise HTTPException(
                status_code=400, detail='Provide the OLD Dependent info you would like to replace.')
        if not amn.new_info:
            raise HTTPException(
                status_code=400, detail='Provide the NEW Dependent info you would like to include.')
        raw = rawUser(reqs)
        new_amend = Amendment(
            amn.idnum, amn.policy, amn.old_info, amn.new_info, {"fullname": raw[0], "token": raw[1]})
        result = opn.save(new_amend)
        # Record into the logs of the new task
        log = my_log(
            raw[0],  raw[1], "New Amendment", "Created a new Amendment: {}".format(amn.policy))
        bgtask.add_task(elog.write, log)
        return {'data': result}
    except Exception:
        raise HTTPException(
            status_code=400, detail="Amendment entry task was unsuccessful, please check and try again.")


@amend_route.get('/similar/{policyno}/{idnumber}/')
async def similar_amendments(policyno: str, idnumber: str, req: Request, bgtask: BackgroundTasks):
    try:
        raw = rawUser(req)
        if not policyno:
            raise HTTPException(
                status_code=400,
                detail='Provide a Policy Number to search for similar entries.')
        if not idnumber:
            raise HTTPException(
                status_code=400,
                detail='Provide an ID number to search for similar entries.')
        data = opn.show_similar(policyno, idnumber)
        log = my_log(
            raw[0], raw[1], "Similar Amendments",
            "Identify Similar Amendments using policy number {}, and id number {}".format(policyno, idnumber))
        bgtask.add_task(elog.write, log)
        return {'data': data}
    except Exception:
        raise HTTPException(
            status_code=400, detail="Similar Amendment records could not be retrieved, please check and try again.")


@amend_route.get('/today')
async def amendments_by_agent_today(req: Request, bgtask: BackgroundTasks):
    try:
        raw = rawUser(req)
        if not raw[0]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info to complete task.')
        if not raw[1]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info with valid details')
        agn = AgentParam(fullname=raw[0], token=raw[1])
        data = opn.show_today(agn.__dict__)
        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "Today Amendments", "Get Today's Amendments")
        bgtask.add_task(elog.write, log)
        return {'data': data}
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Amendment records today by Agent could not be retrieved, please check and try again.")


@amend_route.get('/all')
async def amendments_by_agent_all(reqs: Request, bgtask: BackgroundTasks):
    try:
        raw = rawUser(reqs)
        if not raw[0]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info to complete task.')
        if not raw[1]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info with valid details')
        agn = AgentParam(fullname=raw[0], token=raw[1])
        data = opn.show_overall(agn.__dict__)

        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "All Amendments", "Get All or Overall Amendments")
        bgtask.add_task(elog.write, log)

        # Return results to user
        return {'data': data}
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Overall Amendment records by Agent could not be retrieved")
