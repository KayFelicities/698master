'''IC extract'''
import re
from bs4 import BeautifulSoup


def main():
    '''extract'''
    soup = BeautifulSoup(open('docs/extractor/698IC.html', encoding='utf-8'), "html.parser")
    table_list = soup.find_all('table')
    ic_text = ''
    for count in range(len(table_list) // 3):
        ic_no = count + 1
        table_no = count * 3
        # ic_class = table_list[table_no].parent.previous_sibling.previous_sibling\
        #                 .get_text(' ', strip=True).split()[-1].replace('接口类定义', '')
        ic_tr_list = table_list[table_no].find_all('tr')
        ic_tr_type = ''
        for ic_tr in ic_tr_list:
            ic_td_list = list(map(lambda x: re.sub(r'\n|\r', '', x.get_text(' ', strip=True)), ic_tr.find_all('td')))
            if len(ic_td_list) in [2, 3] and re.match(r'^\d+.*', ic_td_list[0]):
                no = re.split(r'[.．]', ic_td_list[0], 1)[0].strip()
                name = re.split(r'[.．]', ic_td_list[0], 1)[1]
                attr = re.sub(r'（|）|\s', '', ic_td_list[1]) if ic_tr_type == '属性' else ''
                data_type = ic_td_list[2] if ic_tr_type == '属性' else ''
                explain = ''
                others = ''

                expalin_tr_list = table_list[table_no + 1].find_all('tr') if ic_tr_type == '属性'\
                                        else table_list[table_no + 2].find_all('tr')
                for explain_tr in expalin_tr_list:
                    expalin_td_list = list(map(lambda x: re.sub(r'\n|\r', '', x.get_text(' ', strip=True)), explain_tr.find_all('td')))
                    if expalin_td_list[0].strip() == no.strip():
                        explain = expalin_td_list[1].replace('｛', '{').replace('｝', '}') + ' '
                        others = expalin_td_list[2].replace('｛', '{').replace('｝', '}') + ' '

                if ic_tr_type == '方法':
                    # print(explain, 'others:', others)
                    search_type = re.search(r'∷\s{0,2}=\s{0,2}([\w\-]+)[\s\t\n]', explain)
                    if search_type:
                        data_type = search_type.group(1)
                    else:
                        print(explain)
                
                if data_type == 'array':
                    search_array = re.search(r'array\s+.*?[\s\t\n]', explain)
                    if not search_array:
                        search_array = re.search(r'array\s+.*?[\s\t\n]', others)
                    if search_array:
                        data_type = search_array.group()
                        # data_type = re.sub(r'array(.*)', 'array \g<1>', data_type).replace(' ', '')
                data_type = data_type.strip()

                search_explain = re.search(r'([\w\-]+\s{0,2}\{.*\})', explain)
                if not search_explain:
                    search_explain = re.findall(r'∷\s{0,2}=\s{0,2}([\w-]+)', explain)
                    explain = search_explain[-1].replace('，', ',').replace('（', '<').replace('）', '>') if search_explain else ''
                else:
                    explain = search_explain.group(1).replace('，', ',').replace('（', '<').replace('）', '>')

                search_others = re.search(r'([\w-]+\s\{.*\})', others)
                if not search_others:
                    search_others = re.search(r'∷\s+=\s+([\w-]+)', others)
                others = search_others.group(1).replace('，', ',').replace('（', '(').replace('）', ')') if search_others else ''

                structure = explain + others
                structure = structure.strip() if structure.strip() != data_type.strip() else ''
                structure = re.sub(r'\( {1,2}', '(', structure)
                structure = re.sub(r' {1,2}\(', '(', structure)
                structure = re.sub(r' {1,2}\)', ')', structure)
                structure = re.sub(r'\((.*?) {1,2}(,.*?)\)', '(\g<1>\g<2>)',  structure)
                structure = re.sub(r'\((.*?,) {1,2}(.*?)\)', '(\g<1>\g<2>)',  structure)
                structure = re.sub(r'enum\{(.*?)\}', 'enum[\g<1>]', structure)

                structure = re.sub(r'([^-_H])(instance-specific|Data|NULL|array|structure|bool|bit-string|double-long|double-long-unsigned|octet-string|visible-string|UTF8-string|integer|long|unsigned|long-unsigned|long64|long64-unsigned|enum|float32|float64|date_time|date|time|date_time_s|OI|OAD|ROAD|OMD|TI|TSA|MAC|RN|Region|Scaler_Unit|RSD|CSD|MS|SID|SID_MAC|COMDCB|RCSD)([^-_])',\
                                        '\g<1>:\g<2>\g<3>', structure)
                structure = re.sub(r'([^-_H:])(instance-specific|Data|NULL|array|structure|bool|bit-string|double-long|double-long-unsigned|octet-string|visible-string|UTF8-string|integer|long|unsigned|long-unsigned|long64|long64-unsigned|enum|float32|float64|date_time|date|time|date_time_s|OI|OAD|ROAD|OMD|TI|TSA|MAC|RN|Region|Scaler_Unit|RSD|CSD|MS|SID|SID_MAC|COMDCB|RCSD)([^-_])',\
                                        '\g<1>:\g<2>\g<3>', structure)
                structure = structure.replace(' ', '')

                # replace structure,array
                structure = re.sub(r'array(.*?)([,\}])(.*?)\1∷=(:structure{.*?})', 'array\g<4>\g<2>\g<3>', structure)
                structure = re.sub(r',(.*?):structure([,\}])(.*?)\1∷=:structure({.*?})', ',\g<1>:structure\g<4>\g<2>\g<3>', structure)
                structure = re.sub(r'array(.*?)([,\}])(.*?)\1∷=(:structure{.*?})', 'array\g<4>\g<2>\g<3>', structure)
                structure = re.sub(r',(.*?):structure([,\}])(.*?)\1∷=:structure({.*?})', ',\g<1>:structure\g<4>\g<2>\g<3>', structure)

                # 类号，属性/方法，编号，读写属性，属性/方法名，数据类型<单位，换算>(结构)
                ic_text += "('%d', '%s', '%s', '%s', '%s', '%s%s'),\n"\
                                %(ic_no, ic_tr_type.strip(), no, attr,\
                                    name.strip(), data_type.strip(), structure.strip())
                ic_text = ic_text.replace(r'structurestructure', 'structure')
                ic_text = ic_text.replace(r'enumenum', ':enum')
                ic_text = re.sub(r'array([^\{\},]{0,15}[^-_H])(instance|CHOICE|Data|NULL|array|structure|bool|bit-string|double-long|double-long-unsigned|octet-string|visible-string|UTF8-string|integer|long|unsigned|long-unsigned|long64|long64-unsigned|enum|float32|float64|date_time|date|time|date_time_s|OI|OAD|ROAD|OMD|TI|TSA|MAC|RN|Region|Scaler_Unit|RSD|CSD|MS|SID|SID_MAC|COMDCB|RCSD[^-_])', 'array:\g<2>', ic_text)

            else:
                if ic_td_list[0] == '属性':
                    ic_tr_type = '属性'
                if ic_td_list[0] == '方法':
                    ic_tr_type = '方法'
                # print(ic_td_list)

    ic_text =  ic_text.replace('structure {', 'structure{')
    ic_text =  ic_text.replace('CHOICE {', 'CHOICE{')
    ic_text = re.sub(r'enum\{(.*?)\}', 'enum[\g<1>]', ic_text)
    for _ in range(10):
        ic_text = re.sub(r'enum\[(.*?)\((\d+)\)(.*?)\]', 'enum[\g<1><\g<2>>\g<3>]', ic_text)
    ic_text = re.sub(r'< {1,2}(.*?)>', '<\g<1>>',  ic_text)
    ic_text = re.sub(r'<(.*?) {1,2}>', '<\g<1>>',  ic_text)
    ic_text = re.sub(r'<(.*?) {1,2}(,.*?)>', '<\g<1>\g<2>>',  ic_text)
    ic_text = re.sub(r'<(.*?,) {1,2}(.*?)>', '<\g<1>\g<2>>',  ic_text)
    ic_text = re.sub(r'\{ {1,2}(.*?)\}', '{\g<1>}',  ic_text)
    ic_text = re.sub(r'\{(.*?) {1,2}\}', '{\g<1>}',  ic_text)
    ic_text = re.sub(r'\{(.*?) {1,2}(,.*?)\}', '{\g<1>\g<2>}',  ic_text)
    ic_text = re.sub(r'\{(.*?,) {1,2}(.*?)\}', '{\g<1>\g<2>}',  ic_text)

    with open('docs/extractor/ic_extract.txt', 'w', encoding='utf-8') as file:
        file.write(ic_text)


if __name__ == '__main__':
    main()
