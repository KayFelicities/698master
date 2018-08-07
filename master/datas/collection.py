"""msg collections"""
from master import config
import os
import re

collection_file_def = '''# 698后台报文收藏夹
# 手动添加报文请按  显示名称:报文  格式进行编写，保存后刷新或重启软件即可生效
# 删除此文件后重启软件即恢复原始报文收藏夹
# 若您依赖此功能，请注意手动备份以免意外丢失

硬件复位(重启):07 01 00 43 00 01 00 00 00
数据区初始化:07 01 2A 43 00 03 00 00 00
切换rs232功能:07 01 00 f2 00 02 00 16 00 00

清空档案:070105600086000000
下装档案:07010660007F000204120001020A5507050000000000011603160351F2010201090600000000000011041100160312089812000F02045507050000000000000906000000000000120001120001010000
清空任务:070131601281000000
下装任务:07013760127F000101020C110154010005160111011C07E108150000001C0833090909090954010002110216011200001200000202160001010204110011001117113B00
清空普通采集方案:070132601481000000
下装普通采集方案:07013660147F00010102061101120100020211000001035B00001002005B00200002005B00200102005C01160200
清空事件采集方案:070129601681000000
下装事件采集方案:07012E60167F0001010205110102021100010452300006000320220200201E02002020020052300106000320220200201E02002020020052300206000320220200201E02002020020052300306000320220200201E0200202002005C01030012010000
读取抄表数据(方法7):05033A601203000707E1081500000007E10815173B3B000000010400202A020000001002000020000200002001020000

设置事件有效性:06010031000900030100
设置事件上报:06010031000800160300
设置停上电事件参数:06012B31060600020202040408C011181105010002061200011210E01200051200011205281206E000
读取上一条事件(方法9):05033A31060200090104002022020000201E02000020200200002024020000
'''


class Collection():
    """collection class"""
    def __init__(self):
        """init"""
        self.collection_list = []
        if not os.path.isfile(config.COLLECTION_FILE_PATH):
            self.init_collection_file()
        self.refresh_name_list()

    def open_collection_file(self):
        os.system('start "" "notepad" "{dir}"'.format(dir=config.COLLECTION_FILE_PATH))

    def init_collection_file(self):
        if os.path.isfile(config.COLLECTION_FILE_PATH):
            return
        with open(config.COLLECTION_FILE_PATH, 'w', encoding='gbk', errors='ignore') as file:
            file.write(collection_file_def)

    def refresh_name_list(self):
        self.collection_list = []
        if not os.path.isfile(config.COLLECTION_FILE_PATH):
            self.init_collection_file()
        for line in open(config.COLLECTION_FILE_PATH, 'r', encoding='gbk', errors='ignore'):
            if not line.strip() or line.strip()[0] in ['#', '\n', '\r']:
                continue
            re_obj = re.match(r'^(.*?)[:：]([\d\sa-fA-F]+)$', line)
            if re_obj:
                msg_item = (re_obj.group(1), re_obj.group(2))
                self.collection_list.append(msg_item)
            else:
                print('invalid line:', line)

    def get_name_list(self):
        return [x[0] for x in self.collection_list]

    def get_msg(self, name):
        for collection in self.collection_list:
            if name == collection[0]:
                return collection[1]
        return ''
