#coding=utf-8  


def fun1():
    """fun"""
    fun2(2, False)


def fun2(value, is_first):
    """fun"""
    test = [value]
    if is_first:
        fun1()
    print(test)


def fun3(test_list):
    """fun"""
    test_list.pop()

if __name__ == '__main__':
    test_list = [1,2,3,4]
    fun3(test_list)
    print(test_list)

