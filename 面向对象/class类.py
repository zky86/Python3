# -*- coding: utf-8 -*-

# Python面向对象：类，类的方法，类方法，静态方法

class Person(object):
    __test = True
    def __init__(self):

        print('init')

    @staticmethod
    def sayHello(hi):
        if hi is None:
            hi = 'hello'
        print(hi)

    @classmethod
    def hi(cls, msg):
        print(msg)
        print(dir(cls))

    # 一般类的方法
    def hobby(self, hobby):
        print(self.__test)
        print(hobby)


# 调用静态方法，不用实例化
# Person.sayHello('hi')
# Person.hi('Hi!')

# 实例化类调用普通方法,__init__在这里触发
person = Person()
person.hobby('football')
