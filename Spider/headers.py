from pymysql import Connection


conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='xq200431',
    autocommit=True
)
cursor = conn.cursor()  # 获取游标对象
conn.select_db("novels")
class Headers(object):
    def insert_headers(self,name,value):
        insert_query = '''INSERT INTO headers (name, value) VALUES (%s, %s)'''
        cursor.execute(insert_query, (name, value))
        conn.commit()

    # 从数据库中获取头信息
    def get_headers(self):
        select_query = '''SELECT name, value FROM headers'''
        cursor.execute(select_query)
        headers = {}
        for row in cursor.fetchall():
            headers[row[0]] = row[1]
        return headers
    def db_headers(self,headers):
        for name,value in headers.items():
            self.insert_headers(name,value)
if __name__ == "__main__":
    header = Headers()
    headers = {
        'authority': 'cdn.shucdn.com',
        'accept': 'text/css,*/*;q=0.1',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.69xinshu.com/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'style',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    header.db_headers(headers)
    result = header.get_headers()
    print(result)