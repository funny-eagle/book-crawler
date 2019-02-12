# -*- coding: utf-8 -*-
import oss2
import time
import config.config as conf


def connect_oss():
    cfg = conf.config_parser()
    auth = oss2.Auth(cfg.get('oss', 'oss.access_key_id'), cfg.get('oss', 'oss.access_key_secret'))
    bucket = oss2.Bucket(auth, cfg.get('oss', 'oss.endpoint'), cfg.get('oss', 'oss.bucket_name'))
    return bucket


def put_object_from_file(filepath):
    cfg = conf.config_parser()
    bucket = connect_oss()
    current_time = str(round(time.time() * 1000))
    # 一级目录取时间戳的倒数第二位，二级目录去时间戳的倒数第一位
    oss_filepath = cfg.get('oss', 'oss.dir') + current_time[-2:-1] + "/" + current_time[-1:] + "/" + current_time + ".jpg"
    bucket.put_object_from_file(oss_filepath, filepath)
    return oss_filepath, filepath
