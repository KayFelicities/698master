# coding: utf-8
'''OI extract'''
import re
from bs4 import BeautifulSoup


def main():
    '''extract'''
    soup = BeautifulSoup(open('docs/extractor/698OI.html', encoding='utf-8'), "html.parser")
    table_list = soup.find_all('table')
    oi_text = ''
    for table in table_list:
        table_class = table.previous_sibling.previous_sibling\
                        .get_text(' ', strip=True).split()[-1].replace('对象标识定义', '')
        if table_class == '接口类':
            table_class = 'ESAM接口类'
        tr_list = table.find_all('tr')
        for tr in tr_list:
            td_list = tr.find_all('td')
            td_text_list = list(map(lambda x: re.sub(r'\n|\r', ' ', x.get_text(' ', strip=True)), td_list))
            if len(td_text_list) >= 4 and re.match('[0-9a-fA-f]{4}', td_text_list[0].replace(' ', '')):
                oi_no = td_text_list[0].replace(' ', '')
                ic_no = td_text_list[1]
                oi_name = td_text_list[2].replace(' ', '')

                explain = ' ' + td_text_list[3] + ' '

                oi_text += "('{oi}', '{oi_name}', '{ic}', '{ic_name}', '{am_choice}', '{am_no}', '{am_name}', '{data_type}<{unit}|{scaler}>'),\n"\
                                .format(oi=oi_no, oi_name=oi_name, ic=ic_no, ic_name=table_class, am_choice='属性', am_no='0', am_name='',\
                                        data_type='', unit='', scaler='')


                # 对象编号 oi, 对象名 oi_name, 类编号 ic, 类名 ic_name, 属性/方法 am, 属性/方法编号 am_no, 属性/方法名 am_name, 结构 structure
                if table_class == '电能量类':
                    match = re.search(r'电能量∷\s+=([\w-]+).*?单位：\s+([\w-]+).*?换算：\s+([\d-]+).*?高精度电能量∷\s+=([\w-]+).*?单位：\s+([\w-]+).*?换算：\s+([\d-]+)',\
                                        explain)
                    if match:
                        oi_text += "('{oi}', '{oi_name}', '{ic}', '{ic_name}', '{am_choice}', '{am_no}', '{am_name}', '{oi_name}:array:{data_type}<{unit}|{scaler}>,'),\n"\
                                .format(oi=oi_no, oi_name=oi_name, ic=ic_no, ic_name=table_class, am_choice='属性', am_no='2', am_name='',\
                                        data_type=match.group(1), unit=match.group(2), scaler=match.group(3))
                        oi_text += "('{oi}', '{oi_name}', '{ic}', '{ic_name}', '{am_choice}', '{am_no}', '{am_name}', '{oi_name}:array:{data_type}<{unit}|{scaler}>,'),\n"\
                                .format(oi=oi_no, oi_name=oi_name, ic=ic_no, ic_name=table_class, am_choice='属性', am_no='4', am_name='',\
                                        data_type=match.group(4), unit=match.group(5), scaler=match.group(6))
                    else:
                        print('ERROR explain: %s'%explain)
                elif table_class == '最大需量类':
                    match = re.search(r'最大需量值∷\s+=([\w-]+).*?单位：\s+([\w-]+).*?换算：\s+([\d-]+)', explain)
                    if match:
                        oi_text += "('{oi}', '{oi_name}', '{ic}', '{ic_name}', '{am_choice}', '{am_no}', '{am_name}', '{oi_name}:array:{data_type}<{unit}|{scaler}>,'),\n"\
                                .format(oi=oi_no, oi_name=oi_name, ic=ic_no, ic_name=table_class, am_choice='属性', am_no='2', am_name='',\
                                        data_type=match.group(1), unit=match.group(2), scaler=match.group(3))
                    else:
                        print('ERROR explain: %s'%explain)
                elif table_class == '冻结类':
                    oi_text += "('{oi}', '{oi_name}', '{ic}', '{ic_name}', '{am_choice}', '{am_no}', '{am_name}', '{oi_name}:{data_type}<{unit}|{scaler}>,'),\n"\
                            .format(oi=oi_no, oi_name=oi_name, ic=ic_no, ic_name=table_class, am_choice='属性', am_no='2', am_name='',\
                                    data_type='', unit='', scaler='')
                    oi_text = oi_text.replace(r'(,)', '')
                elif table_class in ['变量类', '事件类', '参变量类', '采集监控类', '集合类', '控制类', '文件传输类', 'ESAM接口类', '输入输出设备类', '显示类']:
                    attrs = re.split(r' 属性 | 方法 ', explain)
                    for attr in attrs:
                        attr += '\t'

                        # if oi_no == '8001':
                        #     print('8001:', attr)
                        match = re.search(r'^\s?(\d+)', attr)
                        attr_no = match.group(1).replace(' ', '') if match else '2'
                        am_choice = '属性' if int(attr_no) < 32 else '方法'
                        match = re.search(r'^ {0,2}\d+ {0,2}：? {0,2}(.*?)[∷）\)]', attr)
                        attr_name = match.group(1).strip() if match else ''
                        # attr_name = re.sub(r'^（(.*)$', '\g<1>', attr_name)
                        attr_name = attr_name.replace('（', '(').replace('）', ')')
                        attr_name = re.sub(r'\([^\)]{0,}$', '\g<0>)', attr_name)
                        attr_name = re.sub(r'\( {1,2}', '(', attr_name)
                        attr_name = re.sub(r' {1,2}\(', '(', attr_name)
                        attr_name = re.sub(r' {1,2}\)', ')', attr_name)
                        attr_name = re.sub(r'^\((.*)\)$', '\g<1>', attr_name)
                        attr_name = re.sub(r'[,，]只读', '', attr_name)
                        attr_name = re.sub(r'^只读$', '', attr_name)

                        match = re.search(r'数据类型[：:]\s{0,2}([\w\(\)\-]+)', attr)
                        if not match:
                            match = re.search(r'∷\s{0,2}=\s{0,2}([\w\(\)\-]+)', attr)
                        if not match:
                            match = re.search(r'(structure)', attr)
                        data_type = match.group(1) if match else ''
                        if data_type == 'array':
                            data_type = re.search(r'(array\s{0,2}.*?)\s', attr).group(1)
                        if data_type == 'enum':
                            data_type = re.search(r'(enum\s{0,2}\{.*?\})', attr).group(1).replace(' ', '')
                            data_type = data_type.replace('{', '[')
                            data_type = data_type.replace('}', ']')
                            data_type = data_type.replace('（', '<')
                            data_type = data_type.replace('(', '<')
                            data_type = data_type.replace('）', '>')
                            data_type = data_type.replace(')', '>')
                            data_type = data_type.replace('，', ',')
                        match = re.search(r'(structure\s{0,2}\{.*\})', attr)
                        structure = match.group(0).replace('，', ',').replace('单位：', '').replace('换算：', '') if match else ''
                        structure = re.sub(r'（(.*?)）', '<\g<1>>', structure)
                        if data_type.split(' ')[0] == 'array' and not structure:
                            array_search = re.search(r'(enum\s{0,2}\{.*\})', attr)
                            structure = array_search.group(1).replace('，', ',').replace('（', '<').replace('）', '>').replace(' ', '') if array_search else ''
                        if (ic_no == '1' and (attr_no == '2' or attr_no == '4')) or\
                            (ic_no == '2' and attr_no == '2') or\
                            (ic_no == '3' and attr_no == '2') or\
                            (ic_no == '4' and attr_no == '2') or\
                            (ic_no == '5' and (attr_no == '2' or attr_no == '3' or attr_no == '4')):
                            data_type = 'array:' + data_type

                        structure = structure.replace('enum {', 'enum{')
                        structure = re.sub(r'\( {1,2}', '(', structure)
                        structure = re.sub(r' {1,2}\(', '(', structure)
                        structure = re.sub(r' {1,2}\)', ')', structure)
                        structure = re.sub(r'(.*?) {1,2}(,.*?)', '\g<1>\g<2>', structure)
                        structure = re.sub(r'(.*?,) {1,2}(.*?)', '\g<1>\g<2>', structure)
                        structure = re.sub(r'enum\{(.*?)\}', 'enum[\g<1>]', structure)

                        structure = re.sub(r'([^-_])(Data|NULL|array|structure|bool|bit-string|double-long|double-long-unsigned|octet-string|visible-string|UTF8-string|integer|long|unsigned|long-unsigned|long64|long64-unsigned|enum|float32|float64|date_time|date|time|date_time_s|OI|OAD|ROAD|OMD|TI|TSA|MAC|RN|Region|Scaler_Unit|RSD|CSD|MS|SID|SID_MAC|COMDCB|RCSD)([^-_])',\
                                                '\g<1>:\g<2>\g<3>', structure)
                        structure = re.sub(r'([^-_:])(Data|NULL|array|structure|bool|bit-string|double-long|double-long-unsigned|octet-string|visible-string|UTF8-string|integer|long|unsigned|long-unsigned|long64|long64-unsigned|enum|float32|float64|date_time|date|time|date_time_s|OI|OAD|ROAD|OMD|TI|TSA|MAC|RN|Region|Scaler_Unit|RSD|CSD|MS|SID|SID_MAC|COMDCB|RCSD)([^-_])',\
                                                '\g<1>:\g<2>\g<3>', structure)
                        structure = structure.replace(' ', '')
                        structure = structure.replace('structrue', 'structure')
                        structure = structure.replace('C:OMDCB', 'COMDCB')

                        # replace structure,array
                        structure = re.sub(r'array(.*?)([,\}])(.*?)\1∷=(:structure{.*?})', 'array\g<4>\g<2>\g<3>', structure)
                        structure = re.sub(r',(.*?):structure([,\}])(.*?)\1∷=:structure({.*?})', ',\g<1>:structure\g<4>\g<2>\g<3>', structure)
                        structure = re.sub(r'array(.*?)([,\}])(.*?)\1∷=(:structure{.*?})', 'array\g<4>\g<2>\g<3>', structure)
                        structure = re.sub(r',(.*?):structure([,\}])(.*?)\1∷=:structure({.*?})', ',\g<1>:structure\g<4>\g<2>\g<3>', structure)

                        match = re.search(r'单位[：:]\s{0,2}(.*?)[,，换\t]', attr.split('{')[0])
                        unit = match.group(1).replace(' ', '') if match and data_type != 'structure' else ''
                        match = re.search(r'换算[：:]\s{0,2}(-?\d|无换算)', attr.split('{')[0])
                        scaler = match.group(1).replace(' ', '') if match and data_type != 'structure' else ''

                        if attr_name or data_type or unit or scaler or structure:
                            oi_text += "('{oi}', '{oi_name}', '{ic}', '{ic_name}', '{am_choice}', '{am_no}', '{am_name}', '{brief}{data_type}<{unit}|{scaler}>{structure}{end}'),\n"\
                                    .format(oi=oi_no, oi_name=oi_name, ic=ic_no, ic_name=table_class, am_choice=am_choice, am_no=attr_no, am_name=attr_name,\
                                            brief=((attr_name if attr_name else oi_name) + ':') if data_type or structure else '', data_type=data_type, unit=unit, scaler=scaler,\
                                            structure=structure, end=',' if data_type or structure else '')
                else:
                    print('error')
            else:
                print(td_text_list)
                pass
                
    oi_text = oi_text.replace(r'<|>', '')
    oi_text = oi_text.replace(r'structurestructure', 'structure')
    oi_text = oi_text.replace(r'enumenum', ':enum')
    oi_text = re.sub(r'array([^\{\},]{0,15}[^-_H])(instance|CHOICE|Data|NULL|array|structure|bool|bit-string|double-long|double-long-unsigned|octet-string|visible-string|UTF8-string|integer|long|unsigned|long-unsigned|long64|long64-unsigned|enum|float32|float64|date_time|date|time|date_time_s|OI|OAD|ROAD|OMD|TI|TSA|MAC|RN|Region|Scaler_Unit|RSD|CSD|MS|SID|SID_MAC|COMDCB|RCSD[^-_])', 'array:\g<2>', oi_text)

    oi_text = oi_text.replace('无换算', '0')
    oi_text = oi_text.replace('structure {', 'structure{')
    oi_text = oi_text.replace('enum {', 'enum{')
    oi_text = re.sub(r'enum{(.*?)}', 'enum[\g<1>]', oi_text)
    def replace_hex(match):
        value = int(match.group(1), 16)
        return '<' + str(value) + '>'
    oi_text = re.sub(r'<(\d+)[Hh]>', replace_hex, oi_text)
    oi_text = re.sub(r'< {1,2}(.*?)>', '<\g<1>>', oi_text)
    oi_text = re.sub(r'<(.*?) {1,2}>', '<\g<1>>', oi_text)
    oi_text = re.sub(r'<(.*?) {1,2}([|,].*?)>', '<\g<1>\g<2>>', oi_text)
    oi_text = re.sub(r'<(.*?[|,]) {1,2}(.*?)>', '<\g<1>\g<2>>', oi_text)
    oi_text = re.sub(r'\{ {1,2}(.*?)\}', '{\g<1>}', oi_text)
    oi_text = re.sub(r'\{(.*?) {1,2}\}', '{\g<1>}', oi_text)
    oi_text = re.sub(r'\{(.*?) {1,2}(,.*?)\}', '{\g<1>\g<2>}', oi_text)
    oi_text = re.sub(r'\{(.*?,) {1,2}(.*?)\}', '{\g<1>\g<2>}', oi_text)
    # oi_text = re.sub(r'(<.*?),([\d-]{1,3}>)', '\g<1>|\g<2>', oi_text)

    del_rows = re.findall(r"\('[^,]+', '[^,]+', '[^,]+', '[^,]+', '[^,]+', '[^,]+', '', ''\),", oi_text)
    print(len(del_rows))
    for row in del_rows:
        oiattr = re.search(r"\('([^,]+)', '[^,]+', '[^,]+', '[^,]+', '[^,]+', '[^,]+', '', ''\),", row).group(1)
        if len(re.findall("'%s',"%oiattr, oi_text)) > 1:
            oi_text = re.sub(r"\('%s', '[^,]+', '[^,]+', '[^,]+', '[^,]+', '[^,]+', '', ''\),\n"%oiattr, '', oi_text, 1)

    oi_text = re.sub(r"(\('6000', '[^,]+', '[^,]+', '[^,]+', '属性', '2', '[^,]+'), '(.*?)'\),", "\g<1>, '配置表:array:structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>},扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}}'),", oi_text)
    oi_text = re.sub(r"(\('6000', '[^,]+', '[^,]+', '[^,]+', '方法', '127', '[^,]+'), '(.*?)'\),", "\g<1>, 'array:structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>},扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}}'),", oi_text)
    oi_text = re.sub(r"(\('6000', '[^,]+', '[^,]+', '[^,]+', '方法', '128', '[^,]+'), '(.*?)'\),", "\g<1>, 'array:structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>},扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}}'),", oi_text)
    oi_text = re.sub(r"(\('6001', '[^,]+', '[^,]+', '[^,]+', '属性', '2', '[^,]+'), '(.*?)'\),", "\g<1>, 'structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>},扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}}'),", oi_text)
    oi_text = re.sub(r"(\('6012', '[^,]+', '[^,]+', '[^,]+', '属性', '2', '[^,]+'), '(.*?)'\),", "\g<1>, '配置表:array:structure{任务ID:unsigned,执行频率:TI,方案类型:enum[普通采集方案<1>,事件采集方案<2>,透明方案<3>,上报方案<4>,脚本方案<5>],方案编号:unsigned,开始时间:date_time_s,结束时间:date_time_s,延时:TI,执行优先级:unsigned,状态:enum[正常<1>,停用<2>],任务开始前脚本id:long-unsigned,任务完成后脚本id:long-unsigned,任务运行时段:structure{类型:enum[前闭后开<0>,前开后闭<1>,前闭后闭<2>,前开后开<3>],时段表:array:structure{起始小时:unsigned,起始分钟:unsigned,结束小时:unsigned,结束分钟:unsigned}},}'),", oi_text)
    oi_text = re.sub(r"(\('6012', '[^,]+', '[^,]+', '[^,]+', '方法', '127', '[^,]+'), '(.*?)'\),", "\g<1>, 'array:structure{任务ID:unsigned,执行频率:TI,方案类型:enum[普通采集方案<1>,事件采集方案<2>,透明方案<3>,上报方案<4>,脚本方案<5>],方案编号:unsigned,开始时间:date_time_s,结束时间:date_time_s,延时:TI,执行优先级:unsigned,状态:enum[正常<1>,停用<2>],任务开始前脚本id:long-unsigned,任务完成后脚本id:long-unsigned,任务运行时段:structure{类型:enum[前闭后开<0>,前开后闭<1>,前闭后闭<2>,前开后开<3>],时段表:array:structure{起始小时:unsigned,起始分钟:unsigned,结束小时:unsigned,结束分钟:unsigned}},}'),", oi_text)
    oi_text = re.sub(r"(\('6013', '[^,]+', '[^,]+', '[^,]+', '属性', '2', '[^,]+'), '(.*?)'\),", "\g<1>, '任务配置单元:array:structure{任务ID:unsigned,执行频率:TI,方案类型:enum[普通采集方案<1>,事件采集方案<2>,透明方案<3>,上报方案<4>,脚本方案<5>],方案编号:unsigned,开始时间:date_time_s,结束时间:date_time_s,延时:TI,执行优先级:unsigned,状态:enum[正常<1>,停用<2>],任务开始前脚本id:long-unsigned,任务完成后脚本id:long-unsigned,任务运行时段:structure{类型:enum[前闭后开<0>,前开后闭<1>,前闭后闭<2>,前开后开<3>],时段表:array:structure{起始小时:unsigned,起始分钟:unsigned,结束小时:unsigned,结束分钟:unsigned}},}'),", oi_text)
    oi_text = re.sub(r"(\('6014', '[^,]+', '[^,]+', '[^,]+', '属性', '2', '[^,]+'), '(.*?)'\),", "\g<1>, 'array:structure{方案编号:unsigned,存储深度:long-unsigned,采集方式:structure{采集类型:unsigned,采集内容:Data},记录列选择:array:CSD,电能表集合:MS,存储时标选择:enum[未定义<0>,任务开始时间<1>,相对当日0点0分<2>,相对上日23点59分<3>,相对上日0点0分<4>,相对当月1日0点0分<5>,数据冻结时标<6>相对上月月末0点0分<7>]}'),", oi_text)
    oi_text = re.sub(r"(\('6014', '[^,]+', '[^,]+', '[^,]+', '方法', '127', '[^,]+'), '(.*?)'\),", "\g<1>, 'array:structure{方案编号:unsigned,存储深度:long-unsigned,采集方式:structure{采集类型:unsigned,采集内容:Data},记录列选择:array:CSD,电能表集合:MS,存储时标选择:enum[未定义<0>,任务开始时间<1>,相对当日0点0分<2>,相对上日23点59分<3>,相对上日0点0分<4>,相对当月1日0点0分<5>,数据冻结时标<6>相对上月月末0点0分<7>]}'),", oi_text)

    with open('docs/extractor/oi_extract.txt', 'w', encoding='utf-8') as file:
        file.write(oi_text)

if __name__ == '__main__':
    main()
