from lib2to3.pgen2 import token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from app.audit.audits_controller import AuditLogsController
from app.caller.caller_model import Caller
from app.complains.complains_controller import ComplainsController
from app.utils.auth import AuthHandler
from app.utils.entity import AgentParam, CallerParam, ComplainsParam
from app.utils.quikie import my_log, rawUser

complain_route = APIRouter(
    prefix="/complains", tags=['complains'], dependencies=[Depends(AuthHandler().signed)])
opt = ComplainsController()
elog = AuditLogsController()


@complain_route.post("/")
async def new_complain(com: ComplainsParam, req: Request, bgtask: BackgroundTasks):
    try:
        raw = rawUser(req)
        if not com.info:
            return {'data': "Provide the Complainant details"}
        if not com.msg:
            return {'data': "Provide the Complaint message"}
        if not com.related:
            return {'data': "Provide the Complaint relation option"}
        if not com.specific:
            return {'data': "Provide the Complaint specific option"}
        com.entry_by = {"fullname": raw[1], "token": raw[0]}
        result = opt.save(com)

        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "Client Dependents", "Get All or Listing out Client's Dependentsent")
        bgtask.add_task(elog.write, log)

        # return results to user
        return {'data': result}
    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail="Complaint entry task was unsuccessful")


@complain_route.get("/today")
async def today_complains_agent(req: Request, bgtask: BackgroundTasks):
    try:
        raw = rawUser(req)
        if not raw[1]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info to complete task.')
        if not raw[0]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info with valid details')
        agn = AgentParam(token=raw[1], fullname=raw[0])
        data = opt.show_today(agn.__dict__)

        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "Today's Complaints", "Get Today's Complaints By Agent")
        bgtask.add_task(elog.write, log)

        # return results to user
        return {'data': data}
    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail="Complaint records today by Agent could not be retrieved")


@complain_route.get("/all")
async def overall_complains_agent(req: Request, bgtask: BackgroundTasks):
    try:
        raw = rawUser(req)
        if not raw[1]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info to complete task.')
        if not raw[0]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent credentials info with valid details')
        agn = AgentParam(token=raw[1], fullname=raw[0])
        data = opt.show_all(agn.__dict__)

        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "Overall Complains", "Get All or Overall Related Complains")
        bgtask.add_task(elog.write, log)

        # return results to user
        return {'data': data}
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Overall Complaint records by Agent could not be retrieved")


@complain_route.get("/related")
async def related_complains_agent(category: str, req: Request, bgtask: BackgroundTasks):
    try:
        raw = rawUser(req)
        if not raw[1]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info to complete task.')
        if not raw[0]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent credentials info with valid details')
        if not category:
            raise HTTPException(
                status_code=400,
                detail='Provide a search category to complete task.')
        agn = AgentParam(fullname=raw[0], token=raw[1])
        data = opt.show_related(category, agn.__dict__)

        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "Related Complains", "Get All or Overall Related Complains")
        bgtask.add_task(elog.write, log)

        # return results to user
        return {'data': data}
    except Exception:
        raise HTTPException(
            status_code=400, detail="Related Complaint records by Agent could not be retrieved")
