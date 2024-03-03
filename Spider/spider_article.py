from req import do_request
from pyquery import PyQuery as pq

from spider_for_xinshu69.Spider.headers import Headers
from tasks import Task
from novel_body import Novelbody
import re
from pymysql import Connection

class Spider(object):

    def __init__(self, headers):
        self.headers = headers

    def spider(self, url):
        """
            爬取
        """



        res = do_request(url=url, method="GET", headers=self.headers)
        doc = pq(res.text)
        tag_name_webs = doc('h3')  # 获取书名和网址
        tag_authors_states = doc('label')
        tag_comments = doc('ol')
        # 书名
        novel_name = tag_name_webs.text().split(' ')

        # 书网
        origin_webs = [a.attrib['href'] for a in tag_name_webs('a')]
        for i in range(len(origin_webs)):
            origin_webs[i] = origin_webs[i][:-4] + '/'
        # 作者名和连载状态
        author_state = tag_authors_states.text().split(' ')

        # 简介部分
        comments = tag_comments.items()
        novel_comments = []  # 简介列表
        for item in comments:
            novel_comments.append(item.text())

        # 每个书名所对应的该书的网址，可以通过该书网站爬取所有章节对应的网址
        name_to_webs = {key: value for key, value in zip(novel_name, origin_webs)}

        # 获取每本书的书ID：BID

        pattern = r"book/(\d+)/"
        bid_list = []
        # 遍历网址列表
        for bid in origin_webs:
            # 在网址中查找匹配的内容
            match = re.search(pattern, bid)
            if match:
                # 打印匹配到的部分
                bid_list.append(match.group(1))

        # 将从原始网站，抓取所有章节网址
        def get_total_webs(urls):
            response = do_request(urls, headers=self.headers, method="GET")
            doc = pq(response.text)
            total_webs_list = []
            tag_total_webs = doc('li')('a')
            for i in tag_total_webs.items():
                total_webs = i.attr('href')
                if total_webs != '#':
                    total_webs_list.append(total_webs)
            return total_webs_list

        # 将每本书的所有章节划在一个列表中，一个列表对应一本书，将每个列表放进一个大列表里
        total_webs = []
        for web in origin_webs:

            #try:
            web_list = get_total_webs(web)
            total_webs.append(web_list)


            '''except Exception as e:

                task.status = 'error'
                task.save()'''

        # 得到了大列表  total_webs

        # 对应的作者列表
        author_list = []
        for i in range(0, len(author_state), 3):
            author_list.append(author_state[i])

        # 如果者套流程没问题就将task中的状态改为success，并存入task表中


        return novel_name,author_list,novel_comments,total_webs



if __name__ == "__main__":
    """
        爬取小说
    """
    """headers = {
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
    }"""
    head = Headers()
    headers = head.get_headers()

    url = "https://www.69xinshu.com/novels/hot"
    s = Spider(headers=headers)
    novel_name, author_list, novel_comments, total_webs = s.spider(url)

    conn = Connection(
        host='localhost',
        port=3306,
        user='root',
        password='xq200431',
        autocommit=True
    )
    cursor = conn.cursor()  # 获取游标对象
    conn.select_db("novels")



    for i in range(len(total_webs)):

        bookname = novel_name[i]

        task = Task(title=bookname,chapter_number=0,status="doing")
        try:
            cursor.execute("select * from books where title = %s", (bookname,))
            if not cursor.fetchone():
                cursor.execute("insert into books(title,author,description) values(%s,%s,%s)",
                               (novel_name[i], author_list[i], novel_comments[i]))

            cursor.execute("select id from books where title = %s", (bookname,))

            # bookid = cursor.lastrowid
            result_id = cursor.fetchone()
            bookid = result_id[0]

            cursor.execute("select chapter_number from chapters where book_id = %s", (bookid,))
            if cursor.fetchone():
                cursor.execute("select MAX(chapter_number) AS max_chapter_number from chapters where book_id = %s",
                               (bookid,))
                res_number = cursor.fetchone()
                max_chapter_number = res_number[0]
                while max_chapter_number < len(total_webs[i]):

                    task.chapter_number = max_chapter_number
                    try:
                        getbody = Novelbody(total_webs[i][max_chapter_number], headers)
                        body = getbody.get_novel_body()
                        max_chapter_number += 1
                        cursor.execute("insert into chapters(book_id,chapter_number,title,content) values(%s,%s,%s,%s)",
                                       (bookid, max_chapter_number, f"第{max_chapter_number}章", body))
                        task.chapter_number = max_chapter_number
                        task.status = 'success'
                        task.save()
                    except Exception as e:
                        task.status = 'error'
                        task.save()
                        continue
            else:
                cha_number = 1
                task.chapter_number = 1
                for chapters in total_webs[i]:
                    try:
                        getbody = Novelbody(chapters, headers)
                        body = getbody.get_novel_body()

                        cursor.execute("insert into chapters(book_id,chapter_number,title,content) values(%s,%s,%s,%s)",
                                       (bookid, cha_number, f"第{cha_number}章", body))

                        task.chapter_number = cha_number
                        task.status = 'success'
                        task.save()
                        cha_number += 1
                    except Exception as e:
                        task.status = 'error'
                        task.save()
                        continue
        except Exception as e:
            task.status = 'error'
            task.save()
            continue


