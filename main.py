# -*- coding: utf-8 -*-
import crawler.dangdang.book_crawler as crawler
import urllib
import os
import db.dbutil as db
import datetime
from log.log import Logger
import oss.ossutil as oss
import random
import re

if __name__ == '__main__':
    start = datetime.datetime.now()
    logging = Logger().get_logger()
    logging.info('{0} application running...'.format(start))
    #tempTime = datetime.datetime.now()
    #last_solr_update_time = '2018-12-27 12:19:32'
    #tempTime = datetime.datetime.strptime(last_solr_update_time, '%Y-%m-%d %H:%M:%S')
    id = 653370
    for i in range(0, 10000):
        # 查询需要补充图片的图书
        #selectSQL = '''select b.isbn as isbn, b.properTitle as name, lbs.solr_update from lib_books_sort lbs, books b 
        #                where lbs.isbn = b.isbn and b.imagePathL is null and solr_update <= '{0}'
        #                order by solr_update desc limit 100'''.format(tempTime)
        selectSQL = '''SELECT b.isbn AS isbn, b.properTitle AS name
        FROM lib_books_sort lbs, books b WHERE lbs.isbn = b.isbn AND b.imagePathL IS NULL 
        AND lbs.id>={0} AND lbs.id<{1}'''.format(id, id+100)
        logging.info(selectSQL)
        books = db.select(selectSQL)
        id += 100
        if len(books) == 0:
            continue
        #tempTime = books[len(books)-1][2]
        #logging.info('tempTime={0}'.format(tempTime))
        # 成功计数
        success = 0
        # 失败计数
        failed = 0
        params = []
        # 获取图书信息
        for book in books:
            # isbn非数字或者长度小于10 就跳过
            if book[0] == '' or re.match('^[0-9]*$', book[0]) is None or len(book[0]) < 10:
                logging.warning("illegal isbn-{0}".format(book[0]))
                failed += 1
                continue
            title, isbn, image = crawler.crawl_book_info(book[0])
            if image != '' and isbn != '':
                local_file_path = "F:\\image\\2019-01-11\\{0}\\{1}.jpg".format(random.randint(0, 9), isbn)
                # 下载图书图片到本地
                try:
                    urllib.request.urlretrieve(image, os.path.join(local_file_path))
                except:
                    failed += 1
                    logging.info('{0} http error 400: bad request'.format(image))
                    continue
                logging.info("download {0} image from internet success!".format(isbn))
                # 上传图片到OSS
                oss_filepath, filepath = oss.put_object_from_file(local_file_path)
                logging.info("upload {0} image success!".format(isbn))
                # 拼接 insert batch SQL 参数
                params.append([title, book[1], isbn, image, filepath, oss_filepath, datetime.datetime.now()])
                success += 1
            else:
                logging.warning('{0}-{1} not found!'.format(book[0], book[1]))
                failed += 1

        if success > 0:
            # 批量保存图书信息到数据库
            insertSQL = 'insert ignore into book_crawler (title, name, isbn, img_src, img_local_path, img_oss_url, create_time) values (%s, %s, %s, %s, %s, %s, %s)'
            db.insert_batch(insertSQL, params)
            logging.info("batch insert into book_crawler success!")
            # 查询book_crawler表
            bookList = db.select("select isbn, img_oss_url from book_crawler where status != 1")
            for book in bookList:
                # 更新 book 表 imageURL 字段
                updateSQL = "update books set imagePathL='{0}' where isbn='{1}' and imagePathL is null;".format(book[1], book[0])
                logging.info(updateSQL)
                db.update(updateSQL)
                logging.info("update books success!")
                # 已经更新了book表的，就把book_crawler状态置为1
                updateBookCrawlerSQL = "update book_crawler set status=1 where isbn='{0}'".format(book[0])
                logging.info(updateBookCrawlerSQL)
                db.update(updateBookCrawlerSQL)
                logging.info("update book_crawler success!")

        logging.info('success: {0}, failed: {1}'.format(success, failed))

    end = datetime.datetime.now()
    logging.info('running time:{0}'.format(end - start))
    logging.info('{0} application end!'.format(end))

