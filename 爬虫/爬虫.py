# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


'''
第一个示例：简单的网页爬虫

爬取豆瓣首页
'''

import urllib.request

# 网址
url = "http://www.papercn.cn/"

# 请求
request = urllib.request.Request(url)

# 爬取结果
response = urllib.request.urlopen(request)

data = response.read()

# 设置解码方式
data = data.decode('utf-8')

# 打印结果
print(data)

# 打印爬取网页的各类信息

print(type(response))
print(response.geturl())
print(response.info())
print(response.getcode())


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
#
# # !/usr/bin/python3
#
# a = 21
# b = 10
# c = 0
#
# c = a + b
# print("1 - c 的值为：", c)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
