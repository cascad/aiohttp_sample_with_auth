import json

from aiohttp import web


class CurrentUser(web.View):
    async def post(self):
        resp_form = {"code": 0, "response": self.request.login}
        return web.Response(content_type='application/json', text=json.dumps(resp_form))
