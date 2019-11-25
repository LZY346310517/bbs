from models.model_basic import SQLModel
from models.user import User


class Comment(SQLModel):
    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', -1)
        self.weibo_id = form.get('weibo_id', -1)

    @classmethod
    def add(cls, user_id, form):
        weibo_id = int(form['weibo_id'])
        c = Comment(form)
        c.user_id = user_id
        c.weibo_id = weibo_id
        _id = cls.insert(c.__dict__)
        c.id = _id
        return c

    def user(self):
        u = User.one(id=self.user_id)
        return u
