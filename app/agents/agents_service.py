from fastapi import APIRouter, HTTPException
from app.agents.agents_controller import AgentsController
from app.agents.agents_model import Agent
from app.utils.entity import AgentUser, AuthInfo
from app.utils.auth import AuthHandler

agent_route = APIRouter(prefix="/agents", tags=['agents'])
opt = AgentsController()
aut = AuthHandler()


@agent_route.post("/register", status_code=201)
async def new_registration(agt: AgentUser):
    try:
        if not agt.othername:
            raise HTTPException(
                status_code=400, detail="Agent Otherame is required to continue.")
        if not agt.surname:
            raise HTTPException(
                status_code=400, detail="Agent Surname is required to continue.")
        if not agt.gender:
            raise HTTPException(
                status_code=400, detail="Agent gender is required to continue.")
        if not agt.idnumber:
            raise HTTPException(
                status_code=400, detail="Agent ID Number is required to continue.")
        if not agt.mobile:
            raise HTTPException(
                status_code=400, detail="Agent Mobile or Cellphone number is requried to continue.")
        if not agt.birthdate:
            raise HTTPException(
                status_code=400, detail="Agent Birth date is required to continue.")
        if not agt.email:
            raise HTTPException(
                status_code=400, detail="Agent primary email address is required continue.")
        new_agent = Agent(othername=agt.othername, surname=agt.surname, gender=agt.gender,
                          birthdate=agt.birthdate, mobile=agt.mobile, idnumber=agt.idnumber,
                          email=agt.email, password=aut.hashit(agt.password))
        result = opt.save(new_agent)
        return {'data': result}
    except Exception as ex:
        raise HTTPException(
            status_code=204, detail="Agent entry task was unsuccessful, please check and try again.")


@agent_route.post("/signin", status_code=201)
async def sign_in(info: AuthInfo):
    try:
        if not info.username:
            raise HTTPException(
                status_code=400, detail='Provide a username info to sign in.')
        if not info.password:
            raise HTTPException(
                status_code=400, detail='Provide a password info to sign in.')
        data = opt.login(info.username, info.password)
        return {'data': data}
    except Exception as ex:
        print(str(ex))
        raise HTTPException(
            status_code=204, detail="Agent Login credentials could not be validated, please check and try again.")
