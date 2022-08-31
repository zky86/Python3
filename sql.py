import pymysql


# 获取数据库的版本信息
def get_version_info():
  # 打开数据库连接
  db = pymysql.connect(
    host='127.0.0.1',  # 数据库地址
    port=3306,  # 数据库端口
    user='root',  # 连接数据库的用户
    passwd='abc12345678',  # 连接数据库的密码
    db='test',  # 数据库的库名，需要先在 MySQL 里创建
    charset='utf8mb4'  # 字符集
  )
  # 使用 cursor() 方法创建一个游标对象 cursor
  cursor = db.cursor()
  # 使用 execute()  方法执行 SQL 查询
  cursor.execute("SELECT VERSION()")
  # 使用 fetchone() 方法获取单条数据.
  data = cursor.fetchone()
  print("Database version : %s " % data)
  # 关闭数据库连接
  db.close()


# 如果数据库连接存在我们可以使用execute()方法来为数据库创建表，如下所示创建表EMPLOYEE
def create_table():
  # 打开数据库连接
  db = pymysql.connect(
    host='127.0.0.1',  # 数据库地址
    port=3306,  # 数据库端口
    user='root',  # 连接数据库的用户
    passwd='abc12345678',  # 连接数据库的密码
    db='test',  # 数据库的库名，需要先在 MySQL 里创建
    charset='utf8mb4'  # 字符集
  )
  # 使用 cursor() 方法创建一个游标对象 cursor
  cursor = db.cursor()
  # 使用 execute() 方法执行 SQL，如果表存在则删除
  cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
  # 使用预处理语句创建表
  sql = """CREATE TABLE EMPLOYEE (
             StdID int primary key not null,
             FIRST_NAME  CHAR(20) NOT NULL,
             LAST_NAME  CHAR(20),
             AGE INT,
             SEX CHAR(1),
             INCOME FLOAT )"""
  cursor.execute(sql)
  print("create table success!")
  # 关闭数据库连接
  db.close()


# 增
def insert_data():
  # 打开数据库连接
  db = pymysql.connect(
    host='127.0.0.1',  # 数据库地址
    port=3306,  # 数据库端口
    user='root',  # 连接数据库的用户
    passwd='abc12345678',  # 连接数据库的密码
    db='test',  # 数据库的库名，需要先在 MySQL 里创建
    charset='utf8mb4'  # 字符集
  )
  # 使用cursor()方法获取操作游标
  cursor = db.cursor()
  # SQL 插入语句
  sql = """INSERT INTO EMPLOYEE(StdID,FIRST_NAME,
             LAST_NAME, AGE, SEX, INCOME)
             VALUES (1,'Mac', 'Mohan', 20, '0', 2000)"""
  try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    print("insert success!")
  except:
    # 如果发生错误则回滚
    db.rollback()
    print("insert Error!")
  # 关闭数据库连接
  db.close()


# 删
def delete_data():
  # 打开数据库连接
  db = pymysql.connect(
    host='127.0.0.1',  # 数据库地址
    port=3306,  # 数据库端口
    user='root',  # 连接数据库的用户
    passwd='abc12345678',  # 连接数据库的密码
    db='test',  # 数据库的库名，需要先在 MySQL 里创建
    charset='utf8mb4'  # 字符集
  )
  # 使用cursor()方法获取操作游标
  cursor = db.cursor()
  # SQL 删除语句
  sql = "DELETE FROM EMPLOYEE  WHERE SEX = '0'"
  try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交修改
    db.commit()
  except:
    # 发生错误时回滚
    db.rollback()
  # 关闭连接
  db.close()


# 改
def update_data():
  # 打开数据库连接
  db = pymysql.connect(
    host='127.0.0.1',  # 数据库地址
    port=3306,  # 数据库端口
    user='root',  # 连接数据库的用户
    passwd='abc12345678',  # 连接数据库的密码
    db='test',  # 数据库的库名，需要先在 MySQL 里创建
    charset='utf8mb4'  # 字符集
  )
  # 使用cursor()方法获取操作游标
  cursor = db.cursor()
  # SQL 更新语句
  sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '0'"
  try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
  except:
    # 发生错误时回滚
    db.rollback()
  # 关闭数据库连接
  db.close()


# 查
def query_data():
  # 打开数据库连接
  db = pymysql.connect(
    host='127.0.0.1',  # 数据库地址
    port=3306,  # 数据库端口
    user='root',  # 连接数据库的用户
    passwd='abc12345678',  # 连接数据库的密码
    db='test',  # 数据库的库名，需要先在 MySQL 里创建
    charset='utf8mb4'  # 字符集
  )
  # 使用cursor()方法获取操作游标
  cursor = db.cursor()
  # SQL 查询语句
  # sql = "SELECT * FROM EMPLOYEE \
  #        WHERE INCOME > '%d'" % (1000)
  sql = "SELECT * FROM EMPLOYEE"
  try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
      fname = row[1]
      lname = row[2]
      age = row[3]
      sex = row[4]
      income = row[5]
      # 打印结果
      print("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
            (fname, lname, age, sex, income))
  except:
    print("Error: unable to fetch data")

  # 关闭数据库连接
  db.close()


if __name__ == "__main__":
  get_version_info()
  delete_data()
# query_data()
# query_data()
# get_version_info()
# create_table()
# insert_data()
# update_data()
