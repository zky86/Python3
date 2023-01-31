import requests
from bs4 import BeautifulSoup
import time
import pymysql
import DB
from urllib.request import urlopen, urlretrieve
import os

# 列表
__base_list = 'http://www.papercn.cn/xinwenzixun/list_18_'

# 详情
__base_url = 'http://www.papercn.cn'

# 翻页数量
__num = 1


# 创建多层文件夹
def mkdir(path):
    # 去除首尾的空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        # print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False


# 爬取数据
def get_information(page=0):
    url = __base_list + str(page + 1) + '.html'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html.parser")
    out = soup.find("div", attrs={"class": "liebiao"})
    datas = out.find_all('li')
    datas_list = []
    try:
        for data in datas:
            title = data.find('a').text
            url = data.find('a').attrs['href']
            detail_url = __base_url + str(url)
            detail_r = requests.get(detail_url, headers=headers)
            detail_soup = BeautifulSoup(detail_r.content.decode("utf-8"), "html.parser")
            for items in detail_soup.findAll('a'):
                del items['href']
                del items['target']
            content = detail_soup.find("div", attrs={"class": "content"})
            all_img = content.findAll("img")
            for i, img in enumerate(all_img):
                img_url = __base_url + img["src"]
                path = 'd:' + img["src"]  # 完整路径，包括图片名
                img_name = img["src"].split('/')[-1]  # 获取最后一个图片名
                arr = path.split('/')
                arr.pop()
                local_path = '/'.join(arr)  # 本地存储路径，没有图片名
                # 判断目录是否存在，如果不存在建立目录
                if not os.path.exists(path):
                    mkdir(local_path)
                res = requests.get(img_url)  # 通过requests.get获得图片
                res.raise_for_status()
                with open(path, 'wb') as file_obj:
                    file_obj.write(res.content)
                    print(img_name + " 图片保存成功")
                # urlretrieve(img_url, f"./imgs/swiper-{i}.jpg")
            # content = detail_soup.find("div", attrs={"class": "weizhi"})
            # title = data.find('a', attrs={"class": "truetit"}).text.split()[0]
            # artical_link = "https://bbs.hupu.com" + data.find('a', attrs={"class": "truetit"}).attrs['href']
            # author = data.find('a', class_="aulink").text
            # author_link = data.find('a', class_="aulink").attrs['href']
            # create_time = data.find('a', style="color:#808080;cursor: initial; ").text
            # lastest_reply = data.find('span', class_='endauthor').text
            #
            datas_list.append({"title": title, "content": content})
        # print(datas_list)
    except:
        None
    return datas_list


if __name__ == "__main__":
    connection = pymysql.connect(**DB.config)  # 创建连接
    try:
        cur = connection.cursor()  # 创建游标
        for page in range(__num):
            datas = get_information(page)
            for data in datas:
                # 写入数据库
                cur.execute("INSERT INTO list (title, content) VALUES(%s,%s)", (data['title'], data['content']))
            print("正在爬取第%s页" % (page + 1))
            time.sleep(1)
    except pymysql.Error as e:
        print('数据库错误')
        print(e.args[0], e.args[1])
        connection.rollback()  # 若出错了，则回滚
    finally:
        cur.close()  # 关闭游标
        connection.commit()  # 提交事务
        connection.close()  # 关闭连接
