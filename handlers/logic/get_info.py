import aiohttp
from aiohttp import web
import json


class GetInfo(web.View):
    async def post(self):
        data = await self.request.json()
        uid = data["uid"]

        resp_form = {"code": 0, "response": None}
        return web.Response(content_type='application/json', text=json.dumps(resp_form))
