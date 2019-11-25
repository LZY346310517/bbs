from models.todo import Todo
from route.routes_basic import (
    redirect,
    template,
    current_user,
    html_response,
    login_required,
    response_with_headers,
    json_response)
from utils import log


def index(request):
    """
    todo 首页的路由函数
    """
    u = current_user(request)
    key = 'completed'
    if key in request.query:
        # 只能手动判断，因为 bool(str(False)) == True
        if request.query[key] == 'true':
            index_completed = True
        else:
            index_completed = False
        todos = Todo.all(user_id=u.id, completed=index_completed)
        if index_completed:
            active_index = 'completed'
        else:
            active_index = 'uncompleted'
    else:
        todos = Todo.all(user_id=u.id)
        active_index = 'index'
    log('todo index', active_index)
    uncompleted = len(Todo.all(completed=False))
    return html_response(
        'todo_index.html',
        todos=todos, active_index=active_index, uncompleted=uncompleted
    )


def ajax_all(request):
    u = current_user(request)
    todos = Todo.all(user_id=u.id)
    todos = [t.__dict__ for t in todos]
    return json_response(todos)


def ajax_index(request):
    return html_response('todo_ajax.html')


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    u = current_user(request)
    Todo.add(form, u.id)
    return redirect('/todo')


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo')


def edit(request):
    todo_id = int(request.query['id'])
    t = Todo.one(id=todo_id)
    return html_response(
        'todo_edit.html',
        todo_title=t.title,
        todo_id=str(todo_id)
    )


def update(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    todo_id = int(form['id'])
    todo_title = form['title']

    Todo.update(todo_id, title=todo_title)

    return redirect('/todo')


def complete(request):
    todo_id = int(request.query['id'])
    Todo.complete(todo_id)
    return redirect('/todo')


def complete_all(request):
    Todo.complete_all()
    return redirect('/todo')


def clear_all_completed(request):
    Todo.clear_all_completed()
    return redirect('/todo')


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/todo': login_required(index),
        '/todo/add': login_required(add),
        '/todo/delete': login_required(delete),
        '/todo/edit': login_required(edit),
        '/todo/update': login_required(update),
        '/ajax/todo': login_required(ajax_index),
        '/ajax/all': login_required(ajax_all),
        '/todo/complete': login_required(complete),
        '/todo/complete/all': login_required(complete_all),
        '/todo/clear': login_required(clear_all_completed),
    }
    return d
