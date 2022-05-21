from starlette.responses import Response
import json
from starlette.endpoints import HTTPException
from starlette import status
from starlette.requests import Request
from commands import users
from exceptions import LoginExceptions, RegisterExceptions


async def login(request):
    try:
        request = await Request.json(request)
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{'error' : 'wrong login or password'}")
    else:
        password, login= request.get("password"), request.get("login")
        try:
            user = users.login_command(login=login, password=password)
        except LoginExceptions as e:
            if e.args[0] == "wrong login":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{'error' : '%s'}" % (e.args[0]))
        token = users.token_authorization(login, password, user.id)
        return Response("{'token' : %s}" % token, status_code=status.HTTP_200_OK)


async def register(request):
    try:
        request = await Request.json(request)
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{'error' : 'wrong data'}")
    password, login = request.get("password"), request.get("login")
    try:
        users.register_command(login=login, password=password)
    except RegisterExceptions as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{'error' : '%s'}" % (e.args[0]))
    return Response("{}", status_code=status.HTTP_200_OK)


async def refresh_token(request):
    request = Request.headers.fget(request)
    load = users.token_decoder(request["token"])
    if load:
        login, password, userid = load["login"], load["password"], load["sub"]
        token = users.token_authorization(login, password, userid)
        return Response("{'token' : %s}" % token, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="{}")

