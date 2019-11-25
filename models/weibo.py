from typing import List

from models.follow import Follow
from models.model_basic import SQLModel
from models.comment import Comment
from models.user import User
from utils import log


class Weibo(SQLModel):
    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', -1)

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs

    @classmethod
    def add(cls, user_id, form):
        w = Weibo(form)
        w.user_id = user_id
        _id = cls.insert(w.__dict__)
        w.id = _id
        return w

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def feed(cls, u):
        fs: List[Follow] = Follow.all(follower_id=u.id)
        weibos = []
        for f in fs:
            follwed_weibos = Weibo.all(user_id=f.followed_id)
            weibos.extend(follwed_weibos)
        return weibos

    @classmethod
    def delete_all(cls, id):
        Weibo.delete(id)
        comments = Comment.all(weibo_id=id)
        for comment in comments:
            # 使用了delete
            Comment.delete(comment.id)
