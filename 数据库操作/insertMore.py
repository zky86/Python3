import pymysql

# 创建连接
conn = pymysql.connect(
    host='127.0.0.1',  # 数据库地址
    port=3306,  # 数据库端口
    user='root',  # 连接数据库的用户
    passwd='abc12345678',  # 连接数据库的密码
    db='test',  # 数据库的库名，需要先在 MySQL 里创建
    charset='utf8mb4'  # 字符集
)

# 获取游标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# 一次插入一条数据, 并且使用 pymysql 定义的变量占位符
# 编写语句的时候，字段的顺序需要和上面字段的字典中的 key 的顺序一致

insert_data = [
    ["VMware, Inc., Inc.", "111", "VMware-56 4d 2b 4b 91 1e 48 15-5b d2 73 9c ec 98 da 22", "qfedu.com",
     "3.10.0-957.el7.x86_64", "CentOS Linux release 7.6.1810 (Core)", "Intel(R) Core(TM) i5-5350U CPU @ 1.80GHz"],
    ["VMware, Inc., Inc.", "111", "VMware-56 4d 2b 4b 91 1e 48 15-5b d2 73 9c ec 98 da 22", "qfedu.com",
     "3.10.0-957.el7.x86_64", "CentOS Linux release 7.6.1810 (Core)", "Intel(R) Core(TM) i5-5350U CPU @ 1.80GHz"],
    ["VMware, Inc., Inc.", "111", "VMware-56 4d 2b 4b 91 1e 48 15-5b d2 73 9c ec 98 da 22", "qfedu.com",
     "3.10.0-957.el7.x86_64", "CentOS Linux release 7.6.1810 (Core)", "Intel(R) Core(TM) i5-5350U CPU @ 1.80GHz"]
]

sql = 'INSERT INTO base_info(manufacturer, pod_name, sn,host_name,kernel,os,cpu_name) VALUES (%s, %s, %s, %s, %s, %s, %s)'

try:
    res = cursor.executemany(sql, insert_data)
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print(e)
    conn.rollback()
