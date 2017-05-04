'''handle with 698 applayer'''
import trans.datas as database
import trans.datatype as typedo
import trans.service

def take_applayer(m_list, trans_res):
    '''take app layer'''
    offset = 0
    service_type = m_list[offset]
    if service_type not in ['01', '02', '03', '10', '81', '82', '83', '84', '90']:
        service_type += m_list[offset + 1]
        explain = database.SERVICE.get(service_type, '未知服务')
        trans_res.add_row(m_list[offset:], 2, explain, 0)
        offset += 2
    else:
        explain = database.SERVICE.get(service_type, '未知服务')
        trans_res.add_row(m_list[offset:], 1, explain, 0)
        offset += 1
    service = trans.service.Service(trans_res)
    offset += {
        '01': service.link_request,
        # '02': service.connect_request,
        # '03': service.release_request,
        # '81': service.link_response,
        # '82': service.connect_response,
        # '83': service.release_response,
        # '0501': service.GetRequestNormal,
        # '0502': service.GetRequestNormalList,
        # '0503': service.GetRequestRecord,
        # '0504': service.GetRequestRecordList,
        # '0505': service.GetRequestNext,
        # '8501': service.GetResponseNormal,
        # '8502': service.GetResponseNormalList,
        # '8503': service.GetResponseRecord,
        # '8504': service.GetResponseRecordList,
        # '8505': service.GetResponseNext,
        # '0601': service.SetRequestNormal,
        # '0602': service.SetRequestNormalList,
        # '0603': service.SetThenGetRequestNormalList,
        # '8601': service.SetResponseNormal,
        # '8602': service.SetResponseNormalList,
        # '8603': service.SetThenGetResponseNormalList,
        # '0701': service.ActionRequest,
        # '0702': service.ActionRequestList,
        # '0703': service.ActionThenGetRequestNormalList,
        # '8701': service.ActionResponseNormal,
        # '8702': service.ActionResponseNormalList,
        # '8703': service.ActionThenGetResponseNormalList,
        # '0801': service.ReportResponseList,
        # '0802': service.ReportResponseRecordList,
        # '8801': service.ReportNotificationList,
        # '8802': service.ReportNotificationRecordList,
        # '0901': service.proxy_get_request_list,
        # '0902': service.ProxyGetRequestRecord,
        # '0903': service.ProxySetRequestList,
        # '0904': service.ProxySetThenGetRequestList,
        # '0905': service.ProxyActionRequestList,
        # '0906': service.ProxyActionThenGetRequestList,
        # '0907': service.ProxyTransCommandRequest,
        # '8901': service.ProxyGetResponseList,
        # '8902': service.ProxyGetResponseRecord,
        # '8903': service.ProxySetResponseList,
        # '8904': service.ProxySetThenGetResponseList,
        # '8905': service.ProxyActionResponseList,
        # '8906': service.ProxyActionThenGetResponseList,
        # '8907': service.ProxyTransCommandResponse,
        # '10': service.security_request,
        # '90': service.security_response,
    }.get(service_type)(m_list[offset:])
    # if m_list[0] in ['82', '83', '84', '85', '86', '87', '88', '89']:
    #     offset += take_FollowReport(data[offset:])
    #     offset += take_TimeTag(data[offset:])
    # elif m_list[0] in ['02', '03', '05', '06', '07', '08', '09']:
    #     offset += take_TimeTag(data[offset:])
    return offset

