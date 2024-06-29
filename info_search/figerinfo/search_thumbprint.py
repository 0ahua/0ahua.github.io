import requests
import pprint

def get_header_info(domain):
    # 构造完整的URL（这里假设端口是固定的70，如果不是，可能需要传入端口作为另一个参数）
    url = f"http://{domain}"

    # 发送HTTP请求获取响应
    response = requests.get(url)
    # 获取响应头信息
    headers = response.headers

    # 获取Server头字段，即服务器软件版本
    server = headers.get("Server")

    # 获取其他特定头字段信息，例如X-Powered-By
    powered_by = headers.get("X-Powered-By")

    # Write variables to input.txt file
    with open("result/figerinfo.txt", "w",encoding='utf-8') as file:
        file.write("Headers:\n")
        file.write(pprint.pformat(dict(headers)))
        file.write("\n\nServer:\n")
        file.write("\t"+str(server))
        file.write("\n\nPowered By:\n")
        file.write("\t"+str(powered_by))


# Example usage
# get_header_info("baidu.com")