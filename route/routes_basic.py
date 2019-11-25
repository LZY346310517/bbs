import json
import os

from jinja2 import FileSystemLoader, Environment

from utils import log
from models.user import User
from models.session import Session


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def current_user(request):
    log('current_user', request.cookies)
    if 'session_id' in request.cookies:
        log('current_user session_id 存在')
        session_id = request.cookies['session_id']
        s = Session.one(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.one(id=user_id)
            if u is None:
                return User.guest()
            else:
                return u
    else:
        return User.guest()


def error(request):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    r = '{}\r\n<h1>NOT FOUND</h1>'.format(response_with_headers({}, 404))
    return r.encode()


def response_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.x {} VERY OK\r\nConnection: close\r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def redirect(url, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    h = {
        'Location': url,
    }
    if headers is not None:
        h.update(headers)
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    # HTTP 1.1 302 ok
    # Location: /todo
    #
    r = response_with_headers(h, 302) + '\r\n'
    return r.encode()


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    u = current_user(request)
    body = body.replace('{{username}}', u.username)
    r = header + '\r\n' + body
    return r.encode()


# @login_required
def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query['file']
    path = 'static/{}'.format(filename)

    suffix = filename.split('.')[1]
    content_type_from_suffix = dict(
        gif='image/gif',
        jpg='image/jpg',
        js='application/x-javascript',
        css='text/css'
    )
    content_type = content_type_from_suffix[suffix]
    with open(path, 'rb') as f:
        header = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\n'.format(
            content_type
        )
        r = header.encode() + b'\r\n' + f.read()
        return r


def login_required(route_function):
    """
    modified_route_edit = login_required(route_edit)
    modified_route_edit(request)
    这个函数看起来非常绕
    所以暂时不懂也没关系
    就直接复制粘贴拿来用就好了
    """

    def f(request):
        u = current_user(request)
        if u.is_guest():
            return redirect('/login/view')
        else:
            return route_function(request)

    return f


def initialized_environment():
    path = 'templates'
    log('initialized_environment', path, os.path.abspath(path))
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class GuaTemplate:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        t = cls.e.get_template(filename)
        return t.render(**kwargs)


def html_response(filename, headers=None, **kwargs):
    body = GuaTemplate.render(filename, **kwargs)
    h = {
        'Content-Type': 'text/html',
    }
    if headers is not None:
        h.update(headers)
    header = response_with_headers(h)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data, headers=None):
    body = json.dumps(data, indent=2, ensure_ascii=False)
    h = {
        'Content-Type': 'application/json',
    }
    if headers is not None:
        h.update(headers)
    header = response_with_headers(h)
    r = header + '\r\n' + body
    return r.encode()


def test_route(request):
    return html_response('todo_ajax.html')


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    # f = login_required(route_message)
    # route_index(request)
    # f(request)
    d = {
        '/': route_index,
        '/static': route_static,
        '/test': test_route,
    }
    return d
