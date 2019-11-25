import typing

import pymysql

from utils import log


# noinspection SqlNoDataSourceInspection,SqlResolve
class SQLModel(object):

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '{}'.format(cls.__name__.lower())

    @classmethod
    def new(cls, form):
        # cls(form) 相当于 User(form)
        m = cls(form)
        _id = cls.insert(m.__dict__)
        m.id = _id
        return m

    @classmethod
    def _pymysql_connection(cls):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Lifj9106',
            db='web8',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    @classmethod
    def insert(cls, form: typing.Dict[str, str]):
        # INSERT INTO
        #     `user` (`username`, `password`, `email`)
        # VALUES
        #     (`gua`, `123`, `gua@gua.com`)
        connection = cls._pymysql_connection()
        try:
            sql_keys = []
            sql_values = []
            for k in form.keys():
                sql_keys.append('`{}`'.format(k))
                sql_values.append('%s')
            # `username`, `password`, `email`
            formatted_sql_keys = ', '.join(sql_keys)
            # %s, %s, %s
            formatted_sql_values = ', '.join(sql_values)

            sql_insert = 'INSERT INTO `{}` ({}) VALUES ({});'
            sql_insert = sql_insert.format(
                cls.table_name(), formatted_sql_keys, formatted_sql_values
            )
            log('ORM insert <{}>'.format(sql_insert))

            values = tuple(form.values())
            with connection.cursor() as cursor:
                log('ORM execute <{}>'.format(cursor.mogrify(sql_insert, values)))
                cursor.execute(sql_insert, values)
                _id = cursor.lastrowid
            connection.commit()
        finally:
            connection.close()

        # 先 commit，再关闭链接，再返回
        return _id

    @classmethod
    def one(cls, **kwargs):
        # SELECT * FROM User
        # WHERE
        #   `username`=%s AND `password`=%s
        sql_values = []
        for k in kwargs.keys():
            sql_values.append('`{}`=%s'.format(k))
        # `username`, `password`, `email`
        formatted_sql_value = ' AND '.join(sql_values)
        sql_select = 'SELECT * FROM `{}` WHERE {};'
        sql_select = sql_select.format(
            cls.table_name(),
            formatted_sql_value,
        )
        log('ORM select <{}>'.format(sql_select))

        connection = cls._pymysql_connection()
        values = tuple(kwargs.values())
        try:
            with connection.cursor() as cursor:
                log('ORM execute <{}>'.format(cursor.mogrify(sql_select, values)))
                cursor.execute(sql_select, values)
                result = cursor.fetchone()
                if result is None:
                    return None
                else:
                    m = cls(result)
                return m
        finally:
            log('finally 一定会被执行，就算 在 return 之后')
            connection.close()

    @classmethod
    def all(cls, **kwargs):
        sql_values = []
        if len(kwargs) > 0:
            for k in kwargs.keys():
                sql_values.append('`{}`=%s'.format(k))
        # `username`, `password`, `email`
            formatted_sql_value = ' AND '.join(sql_values)
            sql_select = 'SELECT * FROM `{}` WHERE {};'
            sql_select = sql_select.format(
                cls.table_name(),
                formatted_sql_value,
            )
        else:
            sql_select = 'SELECT * FROM `{}`;'.format(
                cls.table_name(),
            )

        log('ORM select <{}>'.format(sql_select))

        connection = cls._pymysql_connection()
        values = tuple(kwargs.values())
        try:
            with connection.cursor() as cursor:
                log('ORM execute <{}>'.format(cursor.mogrify(sql_select, values)))
                cursor.execute(sql_select, values)
                results = cursor.fetchall()
                ms = [cls(result) for result in results]
                return ms
        finally:
            log('finally 一定会被执行，就算 在 return 之后')
            connection.close()

    @classmethod
    def delete(cls, id):
        sql_delete = 'DELETE FROM {} WHERE `id`=%s'.format(cls.table_name())
        log('ORM delete <{}>'.format(sql_delete))

        connection = cls._pymysql_connection()
        values = (id,)
        with connection.cursor() as cursor:
            log('ORM execute <{}>'.format(cursor.mogrify(sql_delete, values)))
            cursor.execute(sql_delete, values)
        connection.commit()

    @classmethod
    def update(cls, id, **kwargs):
        # UPDATE
        #   `User`
        # SET
        #   `username`='test', `password`='456'
        # WHERE `id`=3;
        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_update = 'UPDATE \n\t{} \nSET \n\t{} \nWHERE `id`=%s'.format(
            cls.table_name(),
            sql_set,
        )
        log('ORM update <{}>'.format(sql_update))

        connection = cls._pymysql_connection()
        values = list(kwargs.values())
        values.append(id)
        values = tuple(values)

        with connection.cursor() as cursor:
            log('ORM execute <{}>'.format(cursor.mogrify(sql_update, values)))
            cursor.execute(sql_update, values)
        connection.commit()


