from fastapi import APIRouter, Depends
from app.registration.registration_controller import RegistrationController
from app.registration.registration_model import Member
from app.utils.auth import AuthHandler
from app.utils.entity import AgentParam


register_route = APIRouter(
    prefix='/registration', tags=['registration'], dependencies=[Depends(AuthHandler().signed)])
reg = RegistrationController()


@register_route.post('/')
def new_registration(mem: Member):
    if not mem.firstname:
        return {'data': 'Provide a firstname to complete task.'}
    if not mem.lastname:
        return {'data': 'Provide a lastname to complete task.'}
    if not mem.gender:
        return {'data': 'Provide a gender to complete task.'}
    if not mem.idno:
        return {'data': 'Provide an id number to complete task.'}
    if not mem.mobile:
        return {'data': 'Provide a mobile number info to complete task.'}
    if not mem.birth_date:
        return {'data': 'Provide a date of birth to complete task.'}
    if not mem.product:
        return {'data': 'Provide a product info to complete task.'}
    if not mem.address:
        return {'data': 'Provide a home address to complete task.'}
    data = reg.save(mem)
    return {'data': data}


@register_route.post('/all')
async def overall_registrations(agn: AgentParam):
    if not agn.token:
        return {'data': 'Provide an agent token info to complete task.'}
    data = reg.overall_registrations(agn.__dict__)
    return {'data': data}


@register_route.post('/today')
async def today_registrations(agn: AgentParam):
    if not agn.token:
        return {'data': 'Provide an agent token info to complete task.'}
    data = reg.today_registrations(agn.__dict__)
    return {'data': data}


@register_route.get('/related')
async def related_registrations():
    return {'data': ''}
