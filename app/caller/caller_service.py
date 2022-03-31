from fastapi import BackgroundTasks, Request, APIRouter, Depends, HTTPException
from app.audit.audits_controller import AuditLogsController
from app.caller.caller_controller import CallersController
from app.caller.caller_model import Caller
from app.utils.auth import AuthHandler
from app.utils.entity import AgentParam, CallerParam
from app.utils.quikie import my_log, rawUser

caller_route = APIRouter(
    prefix="/callers", tags=['callers'], dependencies=[Depends(AuthHandler().signed)])
cop = CallersController()
elog = AuditLogsController()


@caller_route.post("/")
async def new_caller(call: CallerParam, req: Request, bgtask: BackgroundTasks):
    try:
        if not call.fullname:
            raise HTTPException(
                status_code=400,
                detail="Provide the Caller fullname.")
        if not call.gender:
            raise HTTPException(
                status_code=400,
                detail="Provide the Caller gender.")
        if not call.phone_no:
            raise HTTPException(
                status_code=400,
                detail="Provide the Caller Mobile or Phone number")
        if not call.location:
            raise HTTPException(
                status_code=400,
                detail="Provide the Caller Location.")
        if not call.action:
            raise HTTPException(
                status_code=400,
                detail="Provide the Caller Query and action related.")
        if not call.category:
            raise HTTPException(
                status_code=400,
                detail="Provide the Caller Query category")
        raw = rawUser(req)
        call.entry_by = {"token": raw[1], "fullname": raw[0]}
        result = cop.save(call)

        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "New Caller", "Creating a New Caller: {}, {} with contact number {}".format(call.fullname, call.location, call.phone_no))
        bgtask.add_task(elog.write, log)

        # return results to user
        return {'data': result}
    except Exception as ex:
        raise HTTPException(
            status_code=400, detail="Caller entry task was unsuccessful, please check and try again.")


@caller_route.get("/today")
async def today_callers_agent(req: Request, bgtask: BackgroundTasks):
    try:
        raw = rawUser(req)
        if not raw[1]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent token info to complete task.')
        if not raw[1]:
            raise HTTPException(
                status_code=400,
                detail='Provide an agent credentials info with valid details')
        agn = AgentParam(fullname=raw[0], token=raw[1])
        data = cop.show_today(agn.__dict__)

        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "Callers Today", "Get Callers for Today")
        bgtask.add_task(elog.write, log)

        # Return result to user
        return {'data': data}
    except Exception as ex:
        raise HTTPException(
            status_code=400, detail="Caller records today by Agent could not be retrieved")


@caller_route.get("/all")
async def overall_callers_agent(req: Request, bgtask: BackgroundTasks):
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
        agn = AgentParam(fullname=raw[0], token=raw[1])
        data = cop.show_overall(agn.__dict__)

        # Record into the logs of the new task
        log = my_log(raw[0], raw[1], "Overall Callers", "Get Overall Callers")
        bgtask.add_task(elog.write, log)

        # Return result to user
        return {'data': data}
    except Exception:
        raise HTTPException(
            status_code=400, detail="Overall Callers records by Agent could not be retrieved")


@caller_route.get("/related")
async def category_callers_agent(category: str, req: Request, bgtask: BackgroundTasks):
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
        if not category:
            raise HTTPException(
                status_code=400,
                detail='Provide a search category to complete task.')
        agn = AgentParam(fullname=raw[0], token=raw[1])
        data = cop.show_related(category, agn.__dic__)

        # Record into the logs of the new task
        log = my_log(
            raw[0], raw[1], "Related Callers", "Get All Related Callers")
        bgtask.add_task(elog.write, log)

        # return results to user
        return {'data': data}
    except Exception:
        raise HTTPException(
            status_code=400, detail="Related Caller records by Agent could not be retrieved")
