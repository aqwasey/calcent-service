from fastapi import FastAPI
from app.registration.registration_service import register_route
from app.audit.audits_services import audit_route
from app.amendment.amendments_service import amend_route
from app.caller.caller_service import caller_route
from app.complains.complains_service import complain_route
from app.external.clients.clients_service import client_route
from app.external.claims.claims_service import claim_route
from app.agents.agents_service import agent_route

app = FastAPI()
app.include_router(agent_route)
app.include_router(audit_route)
app.include_router(amend_route)
app.include_router(caller_route)
app.include_router(complain_route)
app.include_router(claim_route)
app.include_router(client_route)
app.include_router(register_route)


@app.get('/')
async def index():
    return {'data': 'CRM Call Center - RESTFul Service v1.0 - 2022'}
