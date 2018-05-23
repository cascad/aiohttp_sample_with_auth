import json
from aiohttp import web

from aiohttp_security import forget


class Logout(web.View):
    async def post(self):
        resp_form = {"code": 0, "response": "logged out"}
        response = web.Response(content_type='application/json', text=json.dumps(resp_form))
        await forget(self.request, response)
        return response
