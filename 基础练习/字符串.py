# sentence = 'tom\'s pet is a cat'  # 单引号中间还有单引号，可以转义
# sentence2 = "tom's pet is a cat"  # 也可以用双引号包含单引号
# sentence3 = "tom said:\"hello world!\""
# sentence4 = 'tom said:"hello world"'
#
# print(sentence4)

# words = """
# hello
# world
# abcd"""
# print(words)

# py_str = 'python'
# len(py_str)  # 取长度
# py_str[0]  # 第一个字符
# print(py_str[0])
# 'python'[0]
# py_str[-1]  # 最后一个字符


# atuple = (10, 20, 30, 'bob', 'alice', [1,2,3])
# print(len(atuple))
# 10 in atuple
# print(atuple[2])
# print(atuple[3:5])

# import random
# num = random.randint(1, 10) # 随机生成 1－10 之间的数字
# answer = int(input('guess a number: '))  # 将用户输入的字符转成整数
# if answer > num:
#     print('猜大了')
# elif answer < num:
#     print('猜小了')
# else:
#     print('猜对了')
# print('the number:', num)

# for i in range(1, 10):
#     for j in range(1, i + 1):
#         print('%s*%s=%s' % (j, i, i * j), end=' ')
#     print()


import star

print(star.hi)

star.pstar()
