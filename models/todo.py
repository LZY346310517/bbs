from models.model_basic import SQLModel
from utils import log


class Todo(SQLModel):
    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)
        self.completed = form.get('completed', False)

    @classmethod
    def add(cls, form, user_id):
        t = Todo(form)
        t.user_id = user_id
        cls.insert(t.__dict__)
        log('todo add', t, t.user_id, type(t.user_id))
        return t

    @classmethod
    def complete(cls, id):
        t = Todo.one(id=id)
        completed = not t.completed
        Todo.update(id, completed=completed)

    @classmethod
    def complete_all(cls):
        todo = cls.all(completed=False)
        for t in todo:
            t.update(t.id, completed=True)

    @classmethod
    def clear_all_completed(cls):
        todo = cls.all(completed=True)
        for t in todo:
            t.update(t.id, completed=False)


