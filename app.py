import asyncio
import base64
import sys

import aiohttp_cors
import aiohttp_jinja2
import aiohttp_security
import aiohttp_session
import cryptography
import jinja2
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import routes
from handlers.auth.dict_autz import DictionaryAuthorizationPolicy
from helpers.logger_config import config_logger
from middlewares import login_required_middleware
from settings import *


async def on_shutdown(app):
    pass


async def init(loop):
    app = web.Application(loop=loop)

    app.logger = config_logger()

    if DEBUG:
        # Configure default CORS settings.
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        # Configure CORS on all routes.
        for route, route_info in routes.routes.items():
            resource = cors.add(app.router.add_resource(route_info[1], name=route))
            cors.add(resource.add_route(route_info[0], route_info[2]))
    else:
        # route part
        for route, route_info in routes.routes.items():
            app.router.add_route(route_info[0], route, route_info[1], name=route_info[2])
        # end route part

    # Configure Jinja2
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATE_PATH))

    # Add static
    if DEBUG:
        app.router.add_static(STATIC_URL, STATIC_PATH, name='static')

    secret_key = base64.urlsafe_b64decode(COOKIE_SECRET.encode("utf8"))

    aiohttp_session.setup(app,
                          EncryptedCookieStorage(secret_key, cookie_name=PROJECT_PREFIX.upper(), httponly=False))

    # Setup security
    aiohttp_security.setup(app, SessionIdentityPolicy(), DictionaryAuthorizationPolicy(USERS))
    app.middlewares.append(login_required_middleware)
    # end setup security

    app.on_shutdown.append(on_shutdown)

    return app, app.logger


if sys.platform == 'linux':
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

loop = asyncio.get_event_loop()

app, logger = loop.run_until_complete(init(loop))
web.run_app(app, host=SITE_HOST, port=SITE_PORT)

try:
    loop.run_forever()
except KeyboardInterrupt:
    logger.debug(' Stop server begin')
finally:
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(app.cleanup())
    loop.close()
logger.debug('Stop server end')
