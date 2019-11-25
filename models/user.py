import hashlib
import random

import utils

from models.model_basic import SQLModel
from models.session import Session
from models.user_role import UserRole


# noinspection SqlNoDataSourceInspection,SqlResolve
class User(SQLModel):
    def __init__(self, form):
        super().__init__(form)
        # self.id = form.get('id', '')
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', UserRole.normal)
        # self.role = form.get('role', 'normal')

    @classmethod
    def guest(cls):
        form = dict(
            role=UserRole.guest,
            # role='guest',
            username='【游客】',
            id=-1,
        )
        u = cls(form)
        return u

    def is_guest(self):
        # return self.username == '【游客】'
        # return self.username == User.guest().username
        # return self.role == 'guest'
        return self.role == UserRole.guest

    @classmethod
    def login_user(cls, form):
        password = form['password']
        hashed = cls.salted_password(password)
        u = cls.one(username=form['username'], password=hashed)
        utils.log('login_user', u)
        return u

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

    @staticmethod
    def salted_password(password):
        salt = 'dasdasdhkqjwhejkahjdkhajkshdjk'
        salted = password + salt
        hash = hashlib.sha256(salted.encode()).hexdigest()
        return hash

    @classmethod
    def login(cls, form):
        user_login = cls.login_user(form)
        if user_login is not None:
            # 下面是把用户名存入 cookie 中
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            # session 会话
            # 设置一个随机字符串来当令牌使用
            session_id = random_string()
            Session.new(dict(
                session_id=session_id,
                user_id=user_login.id,
            ))
            result = '登录成功'
        else:
            session_id = ''
            result = '用户名或者密码错误'

        return user_login, result, session_id

    @classmethod
    def register(cls, form):
        u = cls(form)
        if u.validate_register():
            password = form['password']
            hashed = cls.salted_password(password)
            u.password = hashed
            _id = cls.insert(u.__dict__)
            u.id = _id
            result = '注册成功<br> <pre>{}</pre>'.format(u)
        else:
            result = '用户名或者密码长度必须大于2'
        return u, result


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'sdfsdafasfsdfsdwtfgjdfghfg'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s
