"""datas for services"""


FAVORITE_OI = [
    '4000 日期时间',
    '4500 公网通信',
    '4510 以太网通信',
]

BASE_CLASS = [
    '电能量类',
    '最大需量类',
    '变量类',
    '事件类',
    '冻结类',
    '采集监控类',
    '集合类',
    '控制类',
    '文件传输类',
    'ESAM接口类',
    '输入输出设备类',
    '显示类',
]


def get_favorite_oi():
    """['oi explain', ...]"""
    return FAVORITE_OI


def get_base_class():
    """['class1', 'class2', ...]"""
    return BASE_CLASS
