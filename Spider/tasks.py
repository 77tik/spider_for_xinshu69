from pymysql import Connection

class Task(object):
    def __init__(self,title,chapter_number,status):

        self.title = title
        self.chapter_number = chapter_number
        self.status = status

    def save(self):

        conn = Connection(
            host='localhost',
            user='root',
            password='xq200431',
            port=3306,
            autocommit=True
        )

        cursor = conn.cursor()
        conn.select_db('novels')

        cursor.execute('insert into tasks(title,chapter_number,status) values(%s, %s, %s)',(self.title,self.chapter_number,self.status))