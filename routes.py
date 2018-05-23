from handlers.auth.current import CurrentUser
from handlers.auth.login import Login
from handlers.auth.logout import Logout

routes = {
    'login': ('POST', '/api/auth/login/', Login, ()),
    'logout': ('POST', '/api/auth/logout/', Logout, ()),
    'current_user': ('POST', '/api/auth/current/', CurrentUser, ()),

}
