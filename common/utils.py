import uuid
import logging
import colorlog
import sys
from logging import handlers
from common.config_pro import *

# 转换数据是否先清空目标表的数据
is_clean_old_data = True  # 同一次导入任务第一次导入清除
is_sub_clean_old_data = False  # 同一次导入任务第二次导入清除


def get_logger(name=None):
    logger = logging.getLogger(name)

    # 日志级别
    logger.setLevel(logging.INFO)

    # 输出到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))

    # 输出到文件
    file_handler = handlers.RotatingFileHandler('logs.log', maxBytes=8 * 1024 * 1024, backupCount=10, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s"))

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


_logger = get_logger()


def gen_uuid():
    return str(uuid.uuid4()).replace("-", '')


# 根据地区名称获取地区编码
def get_region(cursor, name):
    if not bool(name):
        raise Exception("请传入地区名称")

    # 特殊处理
    if name == '大亚湾经济技术开发区':
        name = '大亚湾西区街道'
    elif name == '仲恺高新技术产业开发区':
        name = '惠城区'

    cursor.execute("select xzqhdm,xzqhmc FROM bd_xzqh WHERE xzqhmc = %s", [name])

    rows_from_sys_xzqh = []
    for row in cursor:
        row_dict = dict(zip(cursor.column_names, row))
        rows_from_sys_xzqh.append(row_dict)

    if len(rows_from_sys_xzqh) > 1:
        raise Exception(f"地区数据不唯一, 区域名称: {name}")
    elif len(rows_from_sys_xzqh) == 0:
        raise Exception(f"没有找到区域对应的编码, 区域名称: {name}")

    return rows_from_sys_xzqh[0]['xzqhdm']


def get_dict(cursor, clazz, value):
    if not bool(clazz):
        raise Exception("请输入字典类型")

    if not bool(value):
        return None

    cursor.execute("SELECT * FROM sys_dict_item WHERE dict_type = %s", [clazz])

    mapping_sys_dict_item_value2id = {}
    for row in cursor:
        row_dict = dict(zip(cursor.column_names, row))
        mapping_sys_dict_item_value2id[row_dict['label']] = row_dict['item_value']

    if len(mapping_sys_dict_item_value2id) == 0:
        raise Exception(f"没有获取到相关字典类型的数据，字典类型：{clazz}")

    if str(value).strip() not in mapping_sys_dict_item_value2id:
        raise Exception(f"字典项中不存在该字典值，【字典类型】: {clazz}；【字典值】：{value}")

    return mapping_sys_dict_item_value2id[str(value).strip()]


def dict_mapping(cursor, dict_type, dict_alias, new_name='', old_name='', message=''):
    assert bool(cursor), "cursor 不能为空"
    assert len(str(dict_type).strip()) > 0, "dict_type 不能为空"

    tmp = get_dict(cursor, dict_type, dict_alias)
    _logger.debug(f"{new_name}-{tmp}-【原表字段{old_name}，{message}，{dict_alias}, 文字转换为 字典表 对应码值】")
    return tmp
