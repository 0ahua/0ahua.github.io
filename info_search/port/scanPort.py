import json
import socket
import threading


def scan_port(host, port, port_info, result_list):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))

        if result == 0:
            port_info_item = port_info.get(str(port), "N/A")
            result_list.append((port, port_info_item))
            print(f"Port {port} is open --> {port_info_item}")

        sock.close()
    except socket.error as e:
        print(f"Error occurred while scanning port {port} on {host}: {e}")


def scan_ports_multithreaded(host, port_info, output_file):
    threads = []
    result_list = []

    for port in port_info:
        t = threading.Thread(target=scan_port, args=(host, int(port), port_info, result_list))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # Write scanned ports and related information to the output file
    with open(output_file, "w", encoding='utf-8') as file:
        for port, info in result_list:
            file.write(f"Port: {port}\nInfo: {info}\n\n")

    print(f"Scanned ports written to {output_file}")


# Example usage
target_host = "jd.com"  # 注意这里应该是一个IP地址或可解析的域名
port_info_file = 'E:\python\FinalProject\info_search\port\port_info.json'
port_file = 'E:\python\FinalProject\info_search\\result\port.txt'

with open(port_info_file, 'r', encoding='utf-8') as f:
    port_info = json.load(f)

#scan_ports_multithreaded(target_host, port_info, port_file)