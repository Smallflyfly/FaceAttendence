# coding=utf-8


import pymysql
import time
import uuid
from examples.face import Face


class FaceSQL(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='111.229.203.174',
            user='root',
            password='password',
            database='face',
            port=3306,
            charset='utf8'
        )

    def process_sql(self, sql, args=()):
        cursor = self.conn.cursor()
        result = []
        try:
            cursor.execute(sql, args)
            result = cursor.fetchall()
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
        finally:
            cursor.close()
            return result


    def save(self, face):
        # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        code = str(uuid.uuid4())
        sql = 'insert into base_face(encoding, name, code, create_time) values (%s, %s, %s, %s)'
        args = (face.encoding, face.name, code, create_time)
        self.process_sql(sql, args)

    def update(self, face):
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = 'update base_face set encoding=%s, name=%s, update_time=%s where id=%s'
        args = (face.encoding, face.name, update_time, face.id)
        self.process_sql(sql, args)

    def select_by_id(self, id):
        sql = "select * from base_face where id = %s"
        args = (id)
        # id 为主键  返回最多一条数据
        result = self.process_sql(sql, args)
        return result[0] if result else None

    def select_by_name(self, name):
        sql = "select * from base_face where name like %s"
        args = (name)
        result = self.process_sql(sql, args)
        return result[0] if result else None

    def find_all_face(self):
        sql = "select * from base_face"
        result = self.process_sql(sql)
        return [Face(face[0], face[1], face[2], face[3], face[4], face[5]) for face in result]


if __name__ == '__main__':
    faceSql = FaceSQL()
    # encoding = '1234567890'
    # name = '鹏'
    # print(faceSql.conn)
    # result = faceSql.select_by_id(1)
    # print(result)
    # face = Face(result)
    # print(face.id)
    # result = faceSql.update(id, encoding, name)
    # result = faceSql.select_by_name("方鹏飞")
    # print(result)


