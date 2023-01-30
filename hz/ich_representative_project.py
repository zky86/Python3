"""
非物质文化遗产
from: hz_culture_city_test ----> tbl_data_culturalheritage
to: okdc-ich ----> ich_representative_project
"""

import mysql.connector
import mysql.connector.pooling
import sys
from common import utils

# print(utils)
_logger = utils.get_logger()

_logger.info("创建数据库连接池")
# 数据库连接池
try:
    pool_from = mysql.connector.pooling.MySQLConnectionPool(**utils.config_from_hz_culture_city, pool_size=4)
    pool_to = mysql.connector.pooling.MySQLConnectionPool(**utils.config_to_okdc_ich, pool_size=4)
    pool_okayxx = mysql.connector.pooling.MySQLConnectionPool(**utils.config_from_okayxx, pool_size=4)
    pool_okdc_communal = mysql.connector.pooling.MySQLConnectionPool(**utils.config_from_okdc_communal, pool_size=4)
except Exception as e:
    _logger.error("创建数据库连接池失败:%s", e)
    sys.exit(1)

con_from = None
cursor_from = None
con_to = None
cursor_to = None
con_okayxx = None
cursor_okayxx = None
con_okdc_communal = None
cursor_okdc_communal = None


def clean_data():
    if utils.is_clean_old_data:
        _logger.info("清理数据库：ich_representative_project")
        cursor_to.execute("truncate ich_representative_project")


def main():
    global con_from, cursor_from, con_to, cursor_to, con_okayxx, cursor_okayxx, con_okdc_communal, cursor_okdc_communal
    try:
        _logger.info("创建数据库连接对象: con_from, con_to, con_okayxx, con_okdc_communal")
        # 数据库连接
        con_from = pool_from.get_connection()
        con_to = pool_to.get_connection()
        con_okayxx = pool_okayxx.get_connection()
        con_okdc_communal = pool_okdc_communal.get_connection()

        # 数据迁移数据处理
        con_to.start_transaction()
        _logger.info("开启 con_to 事务")
        _logger.info("创建数据库指针对象: cursor_from, cursor_to, cursor_okayxx, cursor_okdc_communal")
        cursor_from = con_from.cursor()
        cursor_to = con_to.cursor()
        cursor_okayxx = con_okayxx.cursor()
        cursor_okdc_communal = con_okdc_communal.cursor()

        # 数据迁移
        clean_data()
        transform()

        _logger.info("提交 con_to 事务")
        con_to.commit()
    except mysql.connector.Error as err:
        if bool(con_to):
            _logger.info("回滚 con_to 事务")
            con_to.rollback()
        _logger.error(err)
        raise err


def transform():
    # from sys_hr_organ
    _logger.info("惠州项目表 sys_hr_organ(系统部门表), 转换数据为数字和城区的字典：3:惠阳区, 2:惠城区")
    cursor_from.execute("select * from sys_hr_organ")

    mapping_sys_hr_organ_name2id = {}

    for row in cursor_from:
        row_dict = dict(zip(cursor_from.column_names, row))
        mapping_sys_hr_organ_name2id[row_dict['orgid']] = row_dict['name']

    # from tbl_data_culturalheritage
    cursor_from.execute("select * from tbl_data_culturalheritage")
    rows_from_tbl_data_culturalheritage = []
    for row in cursor_from:
        rows_from_tbl_data_culturalheritage.append(dict(zip(cursor_from.column_names, row)))
    _logger.info("惠州项目表 tbl_data_culturalheritage(非物质文化遗产)，查询出所有的非物质文化遗产，共 %s 条记录",
                 len(rows_from_tbl_data_culturalheritage))

    # to ich_representative_project
    sql_to_insert_ich_representative_project = (
        "INSERT INTO `ich_representative_project` "
        "(`representative_project_id`, `region`, `project_name`, `project_introduction`, `type`, "
        "`evaluate_level`, `protection_req`, `inheritance`, `position`, `historical_origin`, `hc_value`, `inheritor`, "
        "`festive_time`, `event_place`, `project_id`, `remark`, `create_user`, `create_time`, `update_user`, `update_time`, `tenant_id`) "
        "VALUES "
        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    for row in rows_from_tbl_data_culturalheritage:
        _logger.info(">>>>>> 开始处理数据: id:%s, name:%s", row['recid'], row['name'])
        _logger.debug(row)
        row_id, tmp_region, tmp_type, tmp_evaluate_level = prepare(mapping_sys_hr_organ_name2id, row)

        row_to_insert_ich_representative_project = (
            row_id, tmp_region, row['name'], row['remark'], tmp_type, tmp_evaluate_level, row['requires'],
            row['inherit'], row['position'], row['origin'], row['culture'],
            row['heritor'], row['festivetime'],
            row['eventplace'],
            None, None,
            None,
            None,
            None,
            None, 1)
        cursor_to.execute(sql_to_insert_ich_representative_project, row_to_insert_ich_representative_project)
        _logger.debug(cursor_to.statement)
        _logger.info("<<<<<<")


def prepare(mapping_sys_hr_organ_name2id, row):
    row_id = utils.gen_uuid()
    _logger.debug(f"representative_project_id-{row_id}-【全新生成数据ID】")
    # region 数字转地区编码
    tmp_region = utils.get_region(cursor_okdc_communal, mapping_sys_hr_organ_name2id[int(row['region'])])
    _logger.debug(f"region-{tmp_region}-【原表字段region，所在区县，数字转换为 行政区划 表对应码值】")
    # type
    tmp_type = utils.get_dict(cursor_okayxx, "ich_fwzwhyclx", row["type"])
    _logger.debug(f"type-{tmp_type}-【原表字段type，类型，{str(row['type']).strip()}, 文字转换为 字典表 对应码值】")
    # evaluate_level
    try:
        tmp_evaluate_level = utils.get_dict(cursor_okayxx, "ich_fwzwhycpddj", row["level"])
    except Exception as err:
        if row['level'] == '惠州':
            _logger.warning(err)
            _logger.warning('特殊处理，将 惠州 替换会 市级')
            tmp_evaluate_level = utils.get_dict(cursor_okayxx, "ich_fwzwhycpddj", '市级')
        else:
            raise
    _logger.debug(f"evaluate_level-{tmp_evaluate_level}-【原表字段level，类型，{str(row['level']).strip()}, 文字转换为 字典表 对应码值】")
    return row_id, tmp_region, tmp_type, tmp_evaluate_level


if __name__ == "__main__":
    main()
