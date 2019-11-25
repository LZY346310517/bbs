from models.comment import Comment
from models.todo import Todo
from models.user import User
from models.weibo import Weibo

import utils


# noinspection SqlNoDataSourceInspection,SqlResolve
def reset(connection):
    sql_reset1 = '''
    DROP DATABASE `web8`;
    '''
    sql_reset2 = '''
    CREATE DATABASE `web8` 
    DEFAULT CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;
    '''
    sql_reset3 = 'USE `web8`'
    with connection.cursor() as cursor:
        cursor.execute(sql_reset1)
        cursor.execute(sql_reset2)
        cursor.execute(sql_reset3)
        print('重置成功')


# noinspection SqlNoDataSourceInspection,SqlResolve
def create_tables(connection):
    user_table = '''
    CREATE TABLE `user` (
        `id`        INT NOT NULL AUTO_INCREMENT,
        `username`  VARCHAR(255) NOT NULL,
        `password`  VARCHAR(255) NOT NULL,
        `role`      ENUM('guest', 'normal'),
        PRIMARY KEY (`id`)
    );
    '''
    session_table = '''
        CREATE TABLE `session` (
            `id`            INT NOT NULL AUTO_INCREMENT,
            `session_id`    VARCHAR(255) NOT NULL,
            `user_id`       INT NOT NULL,
            `expired_time`  INT NOT NULL,
            PRIMARY KEY (`id`)
        );
    '''
    todo_table = '''
        CREATE TABLE `todo` (
            `id`        INT NOT NULL AUTO_INCREMENT,
            `title`     VARCHAR(255) NOT NULL,
            `user_id`   INT NOT NULL,
            `completed` BOOL NOT NULL,
            PRIMARY KEY (`id`)
        );
    '''
    weibo_table = '''
        CREATE TABLE `weibo` (
            `id`            INT NOT NULL AUTO_INCREMENT,
            `content`       VARCHAR(255) NOT NULL,
            `user_id`       INT NOT NULL,
            PRIMARY KEY (`id`)
        );
    '''
    comment_table = '''
        CREATE TABLE `comment` (
            `id`            INT NOT NULL AUTO_INCREMENT,
            `content`       VARCHAR(255) NOT NULL,
            `user_id`       INT NOT NULL,
            `weibo_id`      INT NOT NULL,
            PRIMARY KEY (`id`)
        );
    '''

    follow_table = '''
        CREATE TABLE `follow` (
            `id`            INT NOT NULL AUTO_INCREMENT,
            `follower_id`   INT NOT NULL,
            `followed_id`   INT NOT NULL,
            PRIMARY KEY (`id`)
        );
    '''

    sql_create_tables = [
        user_table,
        todo_table,
        session_table,
        weibo_table,
        comment_table,
        follow_table,
    ]
    # 用 execute 执行一条 sql 语句
    # cursor 数据库游标
    with connection.cursor() as cursor:
        for sql in sql_create_tables:
            utils.log('ORM execute <{}>'.format(cursor.mogrify(sql)))
            cursor.execute(sql)


def fake_data():
    form = dict(
        username='guest',
        password='123',
    )
    u, result = User.register(form)
    form['username'] = 'guestguest'
    User.register(form)

    form = dict(
        title='test todo',
        user_id=u.id,
    )
    utils.log('todo form', form)
    t = Todo.new(form)

    form = dict(
        content='weibo',
        user_id=u.id,
    )
    w = Weibo.new(form)
    form = dict(
        content='comment',
        user_id=u.id,
        weibo_id=w.id
    )
    w = Comment.new(form)


if __name__ == '__main__':
    c = utils.connection()
    try:
        reset(c)
        create_tables(c)
        fake_data()
    finally:
        c.close()

