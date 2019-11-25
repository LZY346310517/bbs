from models.model_basic import SQLModel


class Follow(SQLModel):
    def __init__(self, form):
        super().__init__(form)
        # 关注者
        self.follower_id = form.get('follower_id', None)
        # 被关注者
        self.followed_id = form.get('followed_id', None)
