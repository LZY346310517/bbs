from models.session import Session
from models.user import User, random_string
from route.routes_basic import current_user, template, response_with_headers, html_response, redirect
from utils import log
from urllib.parse import unquote_plus


def route_login_view(request):
    """
    登录页面的路由函数
    """
    user_current = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)
    return html_response('login.html', result=result, username=user_current.username)


def route_login(request):
    """
    登录页面的路由函数
    """
    form = request.form()
    user, result, session_id = User.login(form)
    if user is not None:
        headers = {'Set-Cookie': 'session_id={}'.format(session_id)}
    else:
        headers = {}
    return redirect('/login/view?result={}'.format(result), headers)


def route_register_view(request):
    user = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)
    return html_response('register.html', result=result, username=user.username)


def route_register(request):
    form = request.form()
    user, result = User.register(form)
    return html_response('register.html', result=result, username=user.username)


def route_dict():
    d = {
        '/login': route_login,
        '/login/view': route_login_view,
        '/register': route_register,
        '/register/view': route_register_view,
    }
    return d
