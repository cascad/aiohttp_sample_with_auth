import json
from aiohttp import web
from aiohttp_security import remember

from handlers.auth.dict_autz import check_credentials
from settings import USERS


class Login(web.View):
    async def post(self):
        data = await self.request.json()
        login = data['login']
        password = data['password']

        resp_form = {}

        verified = await check_credentials(USERS, login, password)

        if verified:
            await remember(self.request, None, login)
            resp_form["code"] = 0
            resp_form["response"] = None
            response = web.Response(content_type='application/json', text=json.dumps(resp_form))
        else:
            resp_form["code"] = 1
            resp_form["response"] = "Invalid username/password combination"
            response = web.Response(content_type='application/json', text=json.dumps(resp_form))

        return response
