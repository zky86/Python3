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
# 获取游标对象
# cursor = conn.cursor()
# ((1,), (2,))
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# [{"id": 1}, {"id": 2}]

# 定义 sql 语句, 创建第一个表 服务器基础信息表 base_info
sql = """
create table base_info
 (id int auto_increment primary key, 
  host_name varchar(64) not null, 
  kernel varchar(64),
  os varchar(64),
  manufacturer varchar(32),
  pod_name varchar(64),
  sn varchar(128),
  cpu_name varchar(64)
)"""

# 执行 sql 语句
cursor.execute(sql)

# 提交更改
conn.commit()

# 关闭游标对象
cursor.close()

# 关闭连接对象
conn.close()
