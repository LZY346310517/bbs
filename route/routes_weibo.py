from models.comment import Comment
from models.follow import Follow
from models.user import User
from models.weibo import Weibo
from route.routes_basic import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    """
    todo 首页的路由函数
    """
    if 'user_id' in request.query:
        user_id = int(request.query['user_id'])
        user = User.one(id=user_id)
    else:
        user = current_user(request)
    weibos = Weibo.all(user_id=user.id)
    return html_response('weibo_index.html', weibos=weibos, user=user)


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    u = current_user(request)
    Weibo.add(u.id, form)
    return redirect('/weibo')


def delete(request):
    weibo_id = int(request.query['weibo_id'])
    Weibo.delete_all(weibo_id)
    return redirect('/weibo')


def edit(request):
    weibo_id = int(request.query['weibo_id'])
    w = Weibo.one(id=weibo_id)
    return html_response(
        'weibo_edit.html',
        weibo_id=str(weibo_id),
        weibo_content=w.content,
    )


def update(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    weibo_id = int(form['weibo_id'])
    weibo_content = form['content']

    Weibo.update(weibo_id, content=weibo_content)

    return redirect('/weibo')


def comment_add(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    u = current_user(request)
    Comment.add(u.id, form)
    return redirect('/weibo')


def comment_edit(request):
    comment_id = int(request.query['comment_id'])
    comment = Comment.one(id=comment_id)
    return html_response(
        'comment_edit.html',
        comment_id=comment.id,
        comment_content=comment.content,
    )


def comment_update(request):
    form = request.form()
    weibo_id = int(form['comment_id'])
    content = form['content']
    Comment.update(weibo_id, content=content)
    return redirect('/weibo')


def comment_delete(request):
    comment_id = int(request.query['comment_id'])
    Comment.delete(comment_id)
    return redirect('/weibo')


def follow(request):
    followed_id = int(request.query['user_id'])
    follower_id = current_user(request).id
    form = dict(
        follower_id=follower_id,
        followed_id=followed_id,
    )
    Follow.new(form)
    return redirect('/weibo')


def feed(request):
    user = current_user(request)
    weibos = Weibo.feed(user)
    return html_response('weibo_feed.html', weibos=weibos, user=user)


def weibo_owner_required(route_function):
    def f(request):
        u = current_user(request)
        if request.method == 'GET':
            weibo_id = int(request.query.get('weibo_id'))
        else:
            weibo_id = int(request.form['weibo_id'])

        weibo = Weibo.one(id=weibo_id)
        if u.id == weibo.user_id:
            return route_function(request)
        else:
            return redirect('/weibo')

    return f


def comment_owner_required(route_function):
    def f(request):
        u = current_user(request)
        if request.method == 'GET':
            comment_id = int(request.query.get('comment_id'))
        else:
            comment_id = int(request.form['comment_id'])
        comment = Comment.one(id=comment_id)
        if u.id == comment.user_id:
            return route_function(request)
        else:
            return redirect('/weibo')

    return f


def weibo_owner_or_comment_owner_required(route_function):
    def f(request):
        u = current_user(request)
        if request.method == 'GET':
            user_id = u.id
            comment_id = int(request.query.get('comment_id', ''))
        else:
            user_id = u.id
            comment_id = int(request.form.get('comment_id', ''))
        comment = Comment.one(id=comment_id)
        weibo = Weibo.one(id=comment.weibo_id)
        if comment.user_id == user_id or weibo.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo')

    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/weibo': login_required(index),
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(delete),
        '/weibo/edit': weibo_owner_required(edit),
        '/weibo/update': login_required(update),
        '/comment/add': login_required(comment_add),
        '/comment/edit': comment_owner_required(comment_edit),
        '/comment/update': login_required(comment_update),
        '/comment/delete': weibo_owner_or_comment_owner_required(comment_delete),
        '/weibo/follow': login_required(follow),
        '/weibo/feed': login_required(feed),
    }
    return d
