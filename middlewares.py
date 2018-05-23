import json
from aiohttp import web
from aiohttp.web import middleware, StaticResource
from aiohttp_security.api import authorized_userid

from handlers.logic.main_view import Main
from settings import DEBUG


@middleware
async def login_required_middleware(request, handler):
    """Middleware that restrict access only for authorized users.

    User is considered authorized if authorized_userid
    returns some value.
    """
    if not isinstance(request, web.BaseRequest):
        msg = ("Incorrect decorator usage. "
               "Expecting `def handler(request)` "
               "or `def handler(self, request)`.")
        raise RuntimeError(msg)

    name = request.match_info.route.name
    is_static = type(request.match_info.route.resource) is StaticResource

    def must_logged_in():
        if DEBUG:
            if is_static:
                return False

        for r in [("POST", "login"), ]:
            if request.method == r[0] and name == r[1]:
                return False

        return True

    if must_logged_in():

        identity = await authorized_userid(request)

        if identity is None:
            # non-registered user has None user_id
            return web.Response(content_type='application/json',
                                text=json.dumps(
                                    {"code": 1, "response": "unauthorized"}))

        request.login = identity

    ret = await handler(request)
    return ret


@middleware
async def frontend_url_middleware(request, handler):
    if request.match_info.http_exception is not None:
        response = await Main(request)
    else:
        response = await handler(request)
    return response
