CREATE TABLE book_crawler (
`id`  int(11) NOT NULL AUTO_INCREMENT,
`name`  varchar(255),
`title`  varchar(255),
`isbn`  varchar(255),
`img_src`  varchar(255),
`img_local_path`  varchar(255),
`img_oss_url`  varchar(255),
`create_time`  datetime,
`status`  int(2) DEFAULT 0 comment '0:未同步books表, 1:已同步books表',
PRIMARY KEY (`id`),
UNIQUE INDEX `idx_isbn` (`isbn`) USING BTREE 
) COMMENT '图书信息爬取日志表';