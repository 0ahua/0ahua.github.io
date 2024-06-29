import requests
import json

def get_icp_info(domain, api_key):
    # 设置API的URL  
    url = 'https://www.apimy.cn/api/icp/newicp'

    # 准备请求的数据  
    payload = {
        'key': api_key,
        'domain': domain  # 假设API接受'domain'作为查询备案信息的参数  
    }

    # 发送POST请求  
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # 如果响应状态码不是200，就主动抛出异常  

        # 解析JSON响应  
        result = response.json()
        return result
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else {err}")
    except ValueError:
        print("Invalid JSON response received.")

    return None


# 用户输入域名
#domain = input("请输入域名: ")

# 这里替换成你的API密钥  
api_key = 'dLPU0F5ySPSI0VVLTvbHYWyeAk7XLQ'  # 请确保使用有效的API密钥

# 调用函数并打印结果
def show_icp_info(domain, api_key):
    icp_info = get_icp_info(domain, api_key)
    if icp_info:
        print("备案信息:")
        print(icp_info)  # 根据API的响应格式，可能需要进一步处理icp_info以提取所需信息
        with open("E:\python\FinalProject\info_search\\result\check.txt", "w",encoding='utf-8') as file:
            file.write(json.dumps(icp_info, indent=4, ensure_ascii=False))
        print("备案信息已写入check.txt文件。")
    else:
        print("无法获取备案信息。")

# show_icp_info("jd.com",api_key)
'''
请输入域名: jd.com
备案信息:
{'code': 200, 
'msg': '请求成功', 
'data': {'updateRecordTime': '2020-04-15 10:01:18', 
        'unitName': '北京京东叁佰陆拾度电子商务有限公司', 
        'status': '1', 
        'serviceLicence': '京ICP备11041704号-3', 
        'natureName': '企业', 
        'mainLicence': '京ICP备11041704号', 
        'limitAccess': '否', 'leaderName': '', 
        'domain': 'jd.com', 
        'contentTypeName': ''}, 
'exec_time': 0.091456, 
'ip': '218.199.207.94'}
'''