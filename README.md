# book-crawler 

> 当当、亚马逊图书图片爬虫

## 处理过程

- 1、查询需要补充图片的图书的`isbn`集合
- 2、遍历并校验`isbn`，使用`isbn`作为关键字进行搜索
- 3、将图片保存到本地，然后再上传到OSS
- 4、拼接insert batch SQL，批量保存图书信息到`book_crawler`表
- 5、更新业务表的图片字段，修改`book_crawler`状态

## 配置文件

book-crawler/config/config.ini

[database]
database.ip=
database.user=
database.password=
database.name=

[oss]
oss.access_key_id=
oss.endpoint=
oss.access_key_secret=
oss.bucket_name=
oss.dir=images/book/

[log]
log.file.path=f:\\book-crawler-log\\crawler-2019-01-11.01.log

## MySQL 建表语句

book-crawler/sql/book_crawler.sql

## 程序入口

book-crawler/main.py
