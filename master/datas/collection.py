"""msg collections"""
from master import config
import os
import re

collection_file_def = '''# 698后台报文收藏夹
# 手动添加报文请按  显示名称:报文  格式进行编写，保存后刷新或重启软件即可生效
# 显示名称前添加唯一序号可以方便检索
# 删除此文件后重启软件即恢复原始报文收藏夹
# 若您依赖此功能，请注意手动备份以免意外丢失

# 1.终端管理
101硬件复位(重启):07 01 00 43 00 01 00 00 00
102数据区初始化:07 01 2A 43 00 03 00 00 00
103切换rs232功能:07 01 00 f2 00 02 00 16 00 00

# 2.采集监控
201清空档案:070105600086000000
202下装档案:07010660007F000204120001020A5507050000000000011603160351F2010201090600000000000011041100160312089812000F02045507050000000000000906000000000000120001120001010000
203清空任务:070131601281000000
204下装任务:07 01 37 60 12 7F 00 01 01 02 0C 11 01 54 01 00 02 16 01 11 01 1C 07 E1 08 15 00 00 00 1C 08 33 09 09 09 09 09 54 01 00 02 11 00 16 01 12 00 00 12 00 00 02 02 16 00 01 01 02 04 11 00 11 00 11 17 11 3B 00
205清空普通采集方案:070132601481000000
206下装普通采集方案:07 01 36 60 14 7F 00 01 01 02 06 11 01 12 01 00 02 02 11 00 00 01 03 5B 00 00 10 02 00 5B 00 20 00 02 00 5B 00 20 01 02 00 5C 01 16 01 00
207清空事件采集方案:070129601681000000
208下装事件采集方案:07012E60167F0001010205110102021100010452300006000320220200201E02002020020052300106000320220200201E02002020020052300206000320220200201E02002020020052300306000320220200201E0200202002005C01030012010000
209读取抄表数据(方法7):05033A601203000707E1081500000007E10815173B3B000000010400202A020000001002000020000200002001020000
210读取日冻结(方法5):05033A601203000507E30B08000000010500202A020000604002000060410200006042020001500402000300100200002002002000020000

# 3.事件相关
301设置事件有效性:06010031000900030100
302设置事件上报:06010031000800160300
303设置停上电事件参数:06012B31060600020202040408C011181105010002061200011210E01200051200011205281206E000
304读取上一条事件(方法9):05033A31060200090104002022020000201E02000020200200002024020000
'''


class Collection():
    """collection class"""
    def __init__(self):
        """init"""
        self.collection_list = []
        if not os.path.isfile(config.COLLECTION_FILE_PATH):
            self.init_collection_file(self)
        self.refresh_name_list()

    @staticmethod
    def open_collection_file(self):
        os.system('start "" "notepad" "{dir}"'.format(dir=config.COLLECTION_FILE_PATH))

    @staticmethod
    def init_collection_file(self):
        if not os.path.isdir(config.CONFIG_DIR):
            os.mkdir(config.CONFIG_DIR)
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
