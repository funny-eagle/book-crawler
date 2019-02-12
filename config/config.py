from configparser import ConfigParser
import os


def config_parser():
    cfg = ConfigParser()
    # 获取当前路径
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    # 合成完整路径
    config_file = curr_dir + os.sep + "config.ini"
    cfg.read(config_file)
    return cfg
