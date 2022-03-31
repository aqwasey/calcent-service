from pprint import pprint
from fastapi import Depends, APIRouter, Header, Request
from app.utils.auth import AuthHandler
from bson.json_util import dumps
import json
from app.utils.auth import AuthHandler
from app.utils.quikie import pssh

demo = APIRouter(
    prefix="/demo", tags=['demo'], dependencies=[Depends(AuthHandler().signed)])


@demo.get("/")
async def index(reqs: Request):
    """ auth = reqs.headers['authorization']
    key = pssh(auth)
    raw = AuthHandler().token_data(key)
    client_host = reqs.client.host
    return {"info": "Home sweet home", "client-host": client_host, "authorization": auth, "token": key, "raw-data": raw}
 """
    pass
